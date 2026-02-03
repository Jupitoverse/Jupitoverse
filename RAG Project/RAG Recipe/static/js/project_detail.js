(function () {
  const projectId = window.RAG_RECIPE_PROJECT_ID;
  if (!projectId) return;
  const API = "/api/projects/" + projectId;

  document.getElementById("project-name-link").textContent = projectId;
  document.getElementById("project-title").textContent = "Project: " + projectId;

  const tabs = document.querySelectorAll(".step-tab");
  const panels = document.querySelectorAll(".step-panel");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const step = tab.dataset.step;
      tabs.forEach((t) => t.classList.remove("active"));
      panels.forEach((p) => p.classList.toggle("active", p.id === "panel-" + step));
      tab.classList.add("active");
      if (step === "monitoring") loadMonitoring();
      if (step === "documents") loadDocList();
      if (step === "excel") loadExcelResults();
    });
  });

  function loadMonitoring() {
    fetch(API + "/monitoring")
      .then((r) => r.json())
      .then((m) => {
        document.getElementById("m-total-calls").textContent = m.total_calls || 0;
        document.getElementById("m-total-tokens").textContent =
          (m.total_input_tokens || 0) + " / " + (m.total_output_tokens || 0);
        document.getElementById("m-total-cost").textContent = (m.total_cost_usd || 0).toFixed(4);
        document.getElementById("m-today-calls").textContent = m.today_calls || 0;
        document.getElementById("m-today-cost").textContent = (m.today_cost_usd || 0).toFixed(4);
        document.getElementById("m-last-tokens").textContent = m.last_call_tokens || 0;
        document.getElementById("m-last-cost").textContent = (m.last_call_cost || 0).toFixed(4);
      })
      .catch(() => {});
  }

  const chatMessages = document.getElementById("chat-messages");
  const chatInput = document.getElementById("chat-input");
  const chatSend = document.getElementById("chat-send");

  chatSend.addEventListener("click", () => {
    const msg = (chatInput.value || "").trim();
    if (!msg) return;
    chatInput.value = "";
    chatMessages.innerHTML += '<div class="msg user">' + escapeHtml(msg) + "</div>";
    chatMessages.scrollTop = chatMessages.scrollHeight;
    fetch(API + "/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg, top_k: 4 }),
    })
      .then((r) => r.json())
      .then((data) => {
        const resp = data.response || data.error || "No response.";
        chatMessages.innerHTML += '<div class="msg bot">' + escapeHtml(resp) + "</div>";
        chatMessages.scrollTop = chatMessages.scrollHeight;
      })
      .catch((e) => {
        chatMessages.innerHTML += '<div class="msg bot error">' + escapeHtml(e.message) + "</div>";
      });
  });

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  const docUpload = document.getElementById("doc-upload");
  const docUploadBtn = document.getElementById("doc-upload-btn");
  const docResult = document.getElementById("doc-result");
  const docList = document.getElementById("doc-list");

  docUploadBtn.addEventListener("click", () => docUpload.click());
  docUpload.addEventListener("change", function () {
    const files = this.files;
    if (!files || files.length === 0) return;
    const form = new FormData();
    for (let i = 0; i < files.length; i++) form.append("files", files[i]);
    docResult.innerHTML = "<p>Uploading...</p>";
    fetch(API + "/documents/upload", { method: "POST", body: form })
      .then((r) => r.json())
      .then((data) => {
        docResult.innerHTML = "<p>Ingested " + (data.ingested || 0) + " chunks from " + (data.files && data.files.length ? data.files.length : 0) + " files.</p>";
        loadDocList();
      })
      .catch((e) => {
        docResult.innerHTML = "<p class='error'>" + escapeHtml(e.message) + "</p>";
      });
    this.value = "";
  });

  function loadDocList() {
    const fileUrl = API + "/documents/file/";
    fetch(API + "/documents/list")
      .then((r) => r.json())
      .then((data) => {
        const files = data.files || [];
        docList.innerHTML = files.length === 0
          ? "<li style='color:var(--text-secondary)'>No files. Use Upload more to add PDF, DOCX, TXT.</li>"
          : files.map((f) => {
              const enc = encodeURIComponent(f);
              return "<li><span class='file-name'>" + escapeHtml(f) + "</span><span class='file-actions'><a href='" + fileUrl + enc + "' target='_blank' rel='noopener'>Open</a> <a href='" + fileUrl + enc + "' download>Download</a></span></li>";
            }).join("");
      })
      .catch(() => { docList.innerHTML = "<li style='color:var(--error-color)'>Error loading list.</li>"; });
  }

  const excelUpload = document.getElementById("excel-upload");
  const excelUploadBtn = document.getElementById("excel-upload-btn");
  const excelResult = document.getElementById("excel-result");
  const excelRows = document.getElementById("excel-rows");
  const excelRowDetail = document.getElementById("excel-row-detail");
  const rowDetailContent = document.getElementById("row-detail-content");
  const rowFeedback = document.getElementById("row-feedback");
  const rowRegenerate = document.getElementById("row-regenerate");
  const rowDetailClose = document.getElementById("row-detail-close");

  excelUploadBtn.addEventListener("click", () => {
    const file = excelUpload.files[0];
    if (!file) {
      excelResult.innerHTML = "<p>Select an Excel file.</p>";
      return;
    }
    const form = new FormData();
    form.append("file", file);
    excelResult.innerHTML = "<p>Processing...</p>";
    fetch(API + "/excel/upload", { method: "POST", body: form })
      .then((r) => r.json())
      .then((data) => {
        excelResult.innerHTML = "<p>Processed " + (data.rows || 0) + " rows.</p>";
        loadExcelResults();
      })
      .catch((e) => {
        excelResult.innerHTML = "<p class='error'>" + e.message + "</p>";
      });
  });

  function loadExcelResults() {
    fetch(API + "/excel/results")
      .then((r) => r.json())
      .then((data) => {
        const rows = data.rows || [];
        excelRows.innerHTML = rows.length === 0
          ? "<p>No results. Upload an Excel file first.</p>"
          : rows.map((r, i) => '<div class="excel-row" data-row="' + r.row_index + '">Row ' + r.row_index + ": " + escapeHtml((r.prompt || "").slice(0, 60)) + "...</div>").join("");
        excelRows.querySelectorAll(".excel-row").forEach((el) => {
          el.addEventListener("click", () => {
            const rowIndex = parseInt(el.dataset.row, 10);
            fetch(API + "/excel/row-result?row_index=" + rowIndex)
              .then((res) => res.json())
              .then((row) => {
                rowDetailContent.textContent = JSON.stringify(row, null, 2);
                rowFeedback.value = row.feedback || "";
                excelRowDetail.dataset.rowIndex = rowIndex;
                excelRowDetail.style.display = "block";
              });
          });
        });
      })
      .catch(() => { excelRows.innerHTML = "<p>Error</p>"; });
  }

  document.getElementById("row-save-feedback").addEventListener("click", () => {
    const rowIndex = parseInt(excelRowDetail.dataset.rowIndex, 10);
    const feedback = rowFeedback.value.trim();
    fetch(API + "/excel/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ row_index: rowIndex, feedback: feedback }),
    })
      .then((r) => r.json())
      .then(() =>
        fetch(API + "/excel/row-result?row_index=" + rowIndex)
          .then((res) => res.json())
          .then((row) => {
            rowDetailContent.textContent = JSON.stringify(row, null, 2);
          })
      );
  });

  rowRegenerate.addEventListener("click", () => {
    const rowIndex = parseInt(excelRowDetail.dataset.rowIndex, 10);
    fetch(API + "/excel/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ row_index: rowIndex, regenerate: true }),
    })
      .then((r) => r.json())
      .then(() => loadExcelResults())
      .then(() => {
        fetch(API + "/excel/row-result?row_index=" + rowIndex)
          .then((res) => res.json())
          .then((row) => { rowDetailContent.textContent = JSON.stringify(row, null, 2); });
      });
  });

  rowDetailClose.addEventListener("click", () => { excelRowDetail.style.display = "none"; });
})();
