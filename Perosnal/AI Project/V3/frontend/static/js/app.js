const API = "";
let token = localStorage.getItem("token");
let user = JSON.parse(localStorage.getItem("user") || "null");

function headers() {
  const h = { "Content-Type": "application/json" };
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

async function api(path, options = {}) {
  const res = await fetch(API + path, { ...options, headers: { ...headers(), ...options.headers } });
  if (res.status === 401) {
    logout();
    window.location.reload();
    throw new Error("Unauthorized");
  }
  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    throw new Error(text || res.statusText);
  }
  if (!res.ok) throw new Error(data.detail || data.message || res.statusText);
  return data;
}

function showView(name) {
  document.querySelectorAll(".view").forEach((el) => (el.style.display = "none"));
  document.querySelectorAll(".nav-link").forEach((el) => el.classList.remove("active"));
  const view = document.getElementById("view-" + name);
  const link = document.querySelector('[data-view="' + name + '"]');
  if (view) view.style.display = "block";
  if (link) link.classList.add("active");
  if (name === "dashboard") loadDashboard();
  if (name === "workflows") loadWorkflows();
  if (name === "tasks") loadTasks();
  if (name === "rater") loadRaterQueue();
  if (name === "reviewer") loadReviewerQueue();
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  token = null;
  user = null;
  document.getElementById("login-wrap").classList.remove("hidden");
  document.getElementById("app-shell").classList.remove("visible");
  document.getElementById("login-wrap").style.display = "flex";
  document.getElementById("app-shell").style.display = "none";
}

function renderApp() {
  if (!token || !user) {
    document.getElementById("login-wrap").style.display = "flex";
    document.getElementById("app-shell").style.display = "none";
    return;
  }
  document.getElementById("login-wrap").style.display = "none";
  document.getElementById("app-shell").style.display = "flex";
  document.getElementById("app-shell").classList.add("visible");
  document.getElementById("user-email").textContent = user.email;
  document.getElementById("user-role").textContent = user.role;
  const canOps = ["ops", "admin"].includes(user.role);
  const canRater = ["rater", "ops", "admin"].includes(user.role);
  const canReviewer = ["reviewer", "ops", "admin"].includes(user.role);
  document.querySelector('[data-view="dashboard"]').style.display = canOps ? "block" : "none";
  document.querySelector('[data-view="workflows"]').style.display = canOps ? "block" : "none";
  document.querySelector('[data-view="tasks"]').style.display = "block";
  document.querySelector('[data-view="rater"]').style.display = canRater ? "block" : "none";
  document.querySelector('[data-view="reviewer"]').style.display = canReviewer ? "block" : "none";
  showView(canOps ? "dashboard" : canRater ? "rater" : "reviewer");
}

// ——— Login ———
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errEl = document.getElementById("login-error");
  errEl.classList.remove("visible");
  errEl.textContent = "";
  try {
    const data = await api("/auth/login", {
      method: "POST",
      body: JSON.stringify({
        email: document.getElementById("email").value.trim(),
        password: document.getElementById("password").value,
      }),
    });
    token = data.access_token;
    user = data.user;
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
    renderApp();
  } catch (err) {
    errEl.textContent = err.message || "Login failed";
    errEl.classList.add("visible");
  }
});

document.getElementById("logout-btn").addEventListener("click", () => {
  logout();
  window.location.reload();
});

document.querySelectorAll(".nav-link").forEach((el) => {
  el.addEventListener("click", (e) => {
    e.preventDefault();
    showView(el.getAttribute("data-view"));
  });
});

// ——— Dashboard (Ops) ———
async function loadDashboard() {
  const wsEl = document.getElementById("dashboard-workspaces");
  const projEl = document.getElementById("dashboard-projects");
  const batchEl = document.getElementById("dashboard-batches");
  const taskEl = document.getElementById("dashboard-tasks");
  try {
    const workspaces = await api("/workspaces");
    wsEl.innerHTML =
      "<h3 style='margin-bottom:0.5rem'>Workspaces</h3>" +
      (workspaces.length
        ? workspaces.map((w) => `<div class="card"><h3>${w.name}</h3><p class="meta">${w.description || "—"}</p></div>`).join("")
        : "<p class='empty-state'>No workspaces. Seed data should have created one.</p>");
    const projects = await api("/projects");
    projEl.innerHTML =
      "<h3 style='margin-bottom:0.5rem'>Projects</h3>" +
      (projects.length
        ? projects
            .map(
              (p) =>
                `<div class="card"><h3>${p.name}</h3><p class="meta">${p.description || "—"} · Stages: ${(p.pipeline_stages || []).join(" → ")}</p></div>`
            )
            .join("")
        : "<p class='empty-state'>No projects.</p>");
    const batches = await api("/batches");
    batchEl.innerHTML =
      "<h3 style='margin-bottom:0.5rem'>Batches</h3>" +
      (batches.length
        ? batches.map((b) => `<div class="card"><h3>${b.name}</h3><p class="meta">Batch ID: ${b.id}</p></div>`).join("")
        : "<p class='empty-state'>No batches.</p>");
    const tasks = await api("/tasks");
    const byStatus = {};
    tasks.forEach((t) => {
      byStatus[t.status] = (byStatus[t.status] || 0) + 1;
    });
    taskEl.innerHTML =
      "<h3 style='margin-bottom:0.5rem'>Tasks</h3>" +
      `<div class="card"><p><strong>Total:</strong> ${tasks.length}</p><p class="meta">pending: ${byStatus.pending || 0} · claimed: ${byStatus.claimed || 0} · in_review: ${byStatus.in_review || 0} · done: ${byStatus.done || 0}</p></div>`;
  } catch (err) {
    wsEl.innerHTML = "<p class='empty-state'>Error: " + err.message + "</p>";
  }
}

// ——— Workflows ———
async function loadWorkflows() {
  const listEl = document.getElementById("workflow-list");
  const detailEl = document.getElementById("workflow-detail");
  detailEl.style.display = "none";
  try {
    const workflows = await api("/workflows");
    listEl.innerHTML =
      workflows.length > 0
        ? "<h4 style='margin-bottom:0.5rem'>Workflow list</h4>" +
          workflows
            .map(
              (w) =>
                `<div class="card"><h3>${escapeHtml(w.name)}</h3><p class="meta">${escapeHtml(w.description || "—")}</p><button type="button" class="btn btn-primary" data-workflow-id="${w.id}">Open</button></div>`
            )
            .join("")
        : "<p class='empty-state'>No workflows. Click « Add workflow » to create one.</p>";
    listEl.querySelectorAll("[data-workflow-id]").forEach((btn) => {
      btn.addEventListener("click", () => openWorkflowDetail(parseInt(btn.getAttribute("data-workflow-id"), 10)));
    });
  } catch (err) {
    listEl.innerHTML = "<p class='empty-state'>Error: " + err.message + "</p>";
  }
}

function openWorkflowDetail(workflowId) {
  document.getElementById("workflow-list").style.display = "none";
  const detailEl = document.getElementById("workflow-detail");
  detailEl.style.display = "block";
  api("/workflows/" + workflowId)
    .then((w) => {
      document.getElementById("workflow-detail-title").textContent = w.name + " — Nodes & edges";
      return Promise.all([api("/workflows/" + workflowId + "/nodes"), api("/workflows/" + workflowId + "/edges")]);
    })
    .then(([nodes, edges]) => {
      const html =
        "<p class='meta'>Nodes: " +
        nodes.map((n) => `<span class="badge badge-claimed">${escapeHtml(n.node_type)}</span> ${escapeHtml(n.name)} (id=${n.id})`).join(", ") +
        "</p><p class='meta'>Edges: " +
        (edges.length ? edges.map((e) => `#${e.from_node_id} → #${e.to_node_id}`).join(", ") : "—") +
        "</p>";
      document.getElementById("workflow-nodes-edges").innerHTML = html;
    })
    .catch((err) => (document.getElementById("workflow-nodes-edges").innerHTML = "<p>Error: " + err.message + "</p>"));
}

document.getElementById("workflow-detail-back").addEventListener("click", () => {
  document.getElementById("workflow-detail").style.display = "none";
  document.getElementById("workflow-list").style.display = "block";
  loadWorkflows();
});

document.getElementById("workflow-add-btn").addEventListener("click", async () => {
  const name = prompt("Workflow name:", "New workflow");
  if (!name) return;
  try {
    await api("/workflows", { method: "POST", body: JSON.stringify({ name, description: "" }) });
    loadWorkflows();
  } catch (err) {
    alert(err.message);
  }
});

// ——— Tasks (one tab with filters and sort) ———
async function loadTasks() {
  const status = document.getElementById("tasks-filter-status").value;
  const sortSel = document.getElementById("tasks-sort");
  const sort = sortSel.value === "created_at_desc" ? "created_at" : sortSel.value;
  const order = sortSel.value === "created_at_desc" ? "desc" : "asc";
  let path = "/tasks?order=" + order;
  if (status) path += "&status=" + encodeURIComponent(status);
  if (sort) path += "&sort=" + encodeURIComponent(sort);
  const wrap = document.getElementById("tasks-table-wrap");
  try {
    const tasks = await api(path);
    wrap.innerHTML =
      "<table class='task-table'><thead><tr><th>ID</th><th>Batch</th><th>Status</th><th>Stage</th><th>Claimed by</th><th>Created</th></tr></thead><tbody>" +
      tasks
        .map(
          (t) =>
            "<tr><td>" +
            t.id +
            "</td><td>" +
            t.batch_id +
            "</td><td><span class='badge badge-" +
            t.status +
            "'>" +
            t.status +
            "</span></td><td>" +
            t.pipeline_stage +
            "</td><td>" +
            (t.claimed_by_id || "—") +
            "</td><td>" +
            new Date(t.created_at).toLocaleString() +
            "</td></tr>"
        )
        .join("") +
      "</tbody></table>";
    if (tasks.length === 0) wrap.innerHTML = "<p class='empty-state'>No tasks match the filters.</p>";
  } catch (err) {
    wrap.innerHTML = "<p class='empty-state'>Error: " + err.message + "</p>";
  }
}

document.getElementById("tasks-apply-filters").addEventListener("click", loadTasks);

// ——— Rater ———
async function loadRaterQueue() {
  const myEl = document.getElementById("rater-my-tasks");
  const curEl = document.getElementById("rater-current-task");
  curEl.style.display = "none";
  curEl.innerHTML = "";
  try {
    const myTasks = await api("/queue/my-tasks");
    myEl.innerHTML =
      myTasks.length > 0
        ? "<h4 style='margin-bottom:0.5rem'>Your claimed tasks</h4>" +
          myTasks
            .map(
              (t) =>
                `<div class="card"><span class="badge badge-claimed">claimed</span> Task #${t.id} · ${(t.content && t.content.text) ? t.content.text.slice(0, 60) + "…" : "—"} <button type="button" class="btn btn-primary" style="margin-top:0.5rem" data-task-id="${t.id}">Annotate</button></div>`
            )
            .join("")
        : "<div class='empty-state'><p>You have no claimed tasks. Click « Get next task » to claim one.</p></div>";
    myEl.querySelectorAll("[data-task-id]").forEach((btn) => {
      btn.addEventListener("click", () => openRaterTask(parseInt(btn.getAttribute("data-task-id"), 10)));
    });
  } catch (err) {
    myEl.innerHTML = "<p class='empty-state'>Error: " + err.message + "</p>";
  }
}

function openRaterTask(taskId) {
  const curEl = document.getElementById("rater-current-task");
  curEl.style.display = "block";
  curEl.innerHTML = "<p>Loading…</p>";
  api("/tasks/" + taskId)
    .then((task) => {
      curEl.innerHTML =
        `<div class="card"><h4>Task #${task.id}</h4><div class="task-content">${escapeHtml((task.content && task.content.text) || JSON.stringify(task.content))}</div>` +
        `<form class="task-form" id="rater-submit-form" data-task-id="${task.id}">` +
        `<label>Sentiment</label><select name="sentiment"><option value="">—</option><option value="positive">Positive</option><option value="neutral">Neutral</option><option value="negative">Negative</option></select>` +
        `<label>Notes (optional)</label><textarea name="notes" placeholder="Optional notes"></textarea>` +
        `<button type="submit" class="btn btn-primary" style="margin-top:1rem">Submit for review</button></div></form>`;
      document.getElementById("rater-submit-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const form = e.target;
        const taskId = parseInt(form.getAttribute("data-task-id"), 10);
        const response = { sentiment: form.sentiment.value, notes: form.notes.value };
        api("/queue/tasks/" + taskId + "/submit", { method: "POST", body: JSON.stringify({ response }) })
          .then(() => {
            curEl.style.display = "none";
            curEl.innerHTML = "";
            loadRaterQueue();
          })
          .catch((err) => alert(err.message));
      });
    })
    .catch((err) => (curEl.innerHTML = "<p>Error: " + err.message + "</p>"));
}

document.getElementById("claim-next-btn").addEventListener("click", async () => {
  try {
    const task = await api("/queue/next");
    if (task) openRaterTask(task.id);
    else alert("No pending tasks available.");
  } catch (err) {
    alert(err.message);
  }
});

// ——— Reviewer ———
async function loadReviewerQueue() {
  const listEl = document.getElementById("reviewer-tasks");
  const curEl = document.getElementById("reviewer-current-task");
  curEl.style.display = "none";
  curEl.innerHTML = "";
  try {
    const tasks = await api("/queue/review");
    listEl.innerHTML =
      tasks.length > 0
        ? tasks
            .map(
              (t) =>
                `<div class="card"><span class="badge badge-in_review">in review</span> Task #${t.id} · ${(t.content && t.content.text) ? t.content.text.slice(0, 60) + "…" : "—"} <button type="button" class="btn btn-primary" style="margin-top:0.5rem" data-task-id="${t.id}">Review</button></div>`
            )
            .join("")
        : "<div class='empty-state'><p>No tasks in review right now.</p></div>";
    listEl.querySelectorAll("[data-task-id]").forEach((btn) => {
      btn.addEventListener("click", () => openReviewerTask(parseInt(btn.getAttribute("data-task-id"), 10)));
    });
  } catch (err) {
    listEl.innerHTML = "<p class='empty-state'>Error: " + err.message + "</p>";
  }
}

function openReviewerTask(taskId) {
  const curEl = document.getElementById("reviewer-current-task");
  curEl.style.display = "block";
  curEl.innerHTML = "<p>Loading…</p>";
  Promise.all([api("/tasks/" + taskId), api("/tasks/" + taskId + "/annotations")])
    .then(([task, annotations]) => {
      const raterAnn = annotations.find((a) => a.pipeline_stage === "L1");
      curEl.innerHTML =
        `<div class="card"><h4>Task #${task.id}</h4><div class="task-content">${escapeHtml((task.content && task.content.text) || JSON.stringify(task.content))}</div>` +
        (raterAnn ? `<div class="annotation-item"><span class="stage">Rater annotation (L1)</span><p>Sentiment: ${raterAnn.response.sentiment || "—"} · Notes: ${raterAnn.response.notes || "—"}</p></div>` : "") +
        `<form class="task-form" id="reviewer-submit-form" data-task-id="${task.id}">` +
        `<label>Your decision (optional edit)</label><select name="sentiment"><option value="">Keep as-is</option><option value="positive">Positive</option><option value="neutral">Neutral</option><option value="negative">Negative</option></select>` +
        `<label>Notes</label><textarea name="notes" placeholder="Optional"></textarea>` +
        `<button type="button" class="btn btn-primary" id="reviewer-approve-btn" style="margin-right:0.5rem">Approve</button><button type="submit" class="btn btn-secondary">Submit with edits</button></div></form>`;
      document.getElementById("reviewer-approve-btn").addEventListener("click", () => {
        api("/queue/review/" + taskId + "/approve", { method: "POST" }).then(() => {
          curEl.style.display = "none";
          loadReviewerQueue();
        }).catch((err) => alert(err.message));
      });
      document.getElementById("reviewer-submit-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const form = e.target;
        const response = { sentiment: form.sentiment.value || (raterAnn && raterAnn.response.sentiment), notes: form.notes.value };
        api("/queue/review/" + taskId + "/submit", { method: "POST", body: JSON.stringify({ response }) })
          .then(() => {
            curEl.style.display = "none";
            loadReviewerQueue();
          })
          .catch((err) => alert(err.message));
      });
    })
    .catch((err) => (curEl.innerHTML = "<p>Error: " + err.message + "</p>"));
}

function escapeHtml(s) {
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}

// Init
renderApp();
