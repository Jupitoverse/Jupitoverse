# Data Annotation Platform — Developer User Guide

This guide describes the **workflow-based design** we follow: configurable workflows with nodes and edges, node types (form, review, API, DB, manual), work queues, and how annotation/labeling (file upload, attributes, review) fits the PRD. It also defines IDs, data visibility, and dummy data (50 Indian users with hierarchy).

---

## 1. Relation to the PRD

The PRD defines:

- **Workspace → Project → Batch → Task → Annotation** hierarchy
- **Configurable pipelines and workflow stages** (e.g. L1 → Review → Done)
- **Rater and Reviewer** interfaces; **queueing, assignment, claim locking**
- **Annotation** = structured response (e.g. labels, attributes) for a task

We implement this by:

- Keeping **Workspace, Project, Batch, Task, Annotation** as the core data model.
- Treating a **Pipeline** as one form of workflow (linear stages). We extend to **Workflows** as directed graphs of **Nodes** and **Edges**.
- **Tasks** are the unit of work. A task can be tied to a **Node** in a workflow. When a node requires **manual work** (e.g. annotate or review), the task appears in a **Work Queue** and is visible to the right users (by role/hierarchy).
- **Annotation/Labeling flow:** User uploads file (image/document), fills form (attributes), submits → task moves to next node (e.g. Review) → appears in **Manager/Reviewer work queue** → reviewer sees only that data in their UI → approve/reject → completion in sequence. **Admin** sees everything; **other users** see only their assigned/own data.

---

## 2. Workflow Model (Graph)

### 2.1 Concepts

- **Workflow** — A directed graph of **Nodes** connected by **Edges**. One workflow can be linked as a **child workflow** from a node of another workflow; completion of the child follows its sequence and then control returns to the parent.
- **Node** — A single step in the workflow. Each node has a **unique ID** (e.g. `node_uuid`). Node **type** determines behavior (see below).
- **Node instance** — A running occurrence of a node for a given **task** or **workflow instance**. Each instance has a **unique ID** (e.g. `instance_uuid`). Used for tracking state and sequencing.
- **Workflow instance** — One execution of a workflow for a given root task (or batch). Has a unique **instance ID**.
- **Edge** — Directed link from one node to another (source_node_id → target_node_id). Defines allowed transitions.

### 2.2 Node Types

| Type | Description | Behavior |
|------|-------------|----------|
| **form** | User fills a form (e.g. annotation attributes) | Renders a schema-driven form; on submit, data is stored and flow moves to next node(s). Can support file/image upload and manual attributes. |
| **review** | Manual review step | Task goes into a **work queue** (e.g. Manager/Reviewer queue). Assignee sees task in their UI; they approve, reject, or edit. Completion advances the workflow. |
| **api_call** | System calls an external API | Backend performs HTTP call; result can be stored or used to decide next edge. No user interaction. |
| **db_update** | System updates database | Backend updates DB (e.g. status, metadata). No user interaction. |
| **manual** | Generic manual step | Like review: task is assigned to a **work queue**; a user (by role/hierarchy) claims and completes it; completion advances the workflow. |

Any node that requires **manual work** (form with user input, review, manual) creates or updates a **task** and puts it in the appropriate **work queue** so that the right users see it in their UI.

### 2.3 Work Queue and Assignment

- **Work queue** — Set of tasks (or “work items”) that are **eligible** for a group of users (e.g. by role: Reviewer, Manager) or by hierarchy (e.g. reportees of a manager).
- Tasks in a queue are **assigned** (automatically or manually) to users. **FIFO** and **claim locking** (one task claimed by one user at a time) apply as in the PRD.
- **User UI:** Each user has a **Tasks** tab that shows:
  - Tasks assigned to them (or claimable by them), with **filters and sorting** (e.g. by status, workflow, created date, priority).
  - Only **data they are allowed to see** (see Data Visibility below).

### 2.4 Child Workflows

- A **node** in a parent workflow can be configured to **start a child workflow** (link to another workflow by ID).
- When execution reaches that node, the **child workflow** is started (with its own instance ID). The parent **waits** until the child workflow completes (or a designated exit node).
- Completion is **sequential**: child runs to completion, then the parent continues to the next node(s). This matches “completion will be in that sequence only.”

### 2.5 Identifiers

- **Node ID** — Unique per node definition (e.g. UUID). Same for every execution of that node.
- **Node instance ID** — Unique per execution of a node for a given workflow instance (e.g. UUID). Identifies “this particular run of this node.”
- **Workflow instance ID** — Unique per run of a workflow (e.g. UUID). Ties together all node instances and tasks for that run.

---

## 3. Annotation / Labeling Flow (PRD Alignment)

The main use case is **annotation or labeling** of data (e.g. images, files) with manual attributes and review:

1. **Upload** — User (or system) uploads a file (image, document) and creates a **task** (or batch of tasks) tied to a workflow.
2. **Form node** — User sees a form: uploaded asset + fields (labels, attributes). They fill and submit. Data is stored as **Annotation** (or equivalent); task moves to next node.
3. **Review node (manual)** — Task enters the **review work queue**. Managers/Reviewers see in **their UI** only tasks in their queue. They see the data (asset + attributes) and approve or reject (and optionally edit). Completion moves the workflow to the next node.
4. **Downstream nodes** — May include API call (e.g. send result elsewhere), DB update (e.g. mark as delivered), or another manual step.

**Data visibility:**

- **Admin** — Can see all workflows, all tasks, all queues, all users’ data (full operational view).
- **Other users** — See only:
  - Tasks **assigned to them** or **claimable by them** (by role/hierarchy), and
  - The **data attached to those tasks** (e.g. asset, form response, review outcome).

So: **Admin sees everything; rest is user-wise.**

---

## 4. Data Model (Workflow Extension)

Beyond the core PRD entities (Workspace, Project, Batch, Task, Annotation, User), we add:

- **Workflow** — id, name, project_id (or batch/project scope), version, is_child_allowed, created_at.
- **Node** — id (unique), workflow_id, type (form | review | api_call | db_update | manual), config (JSON: schema for form, API URL for api_call, etc.), order/position for display.
- **Edge** — id, workflow_id, source_node_id, target_node_id, condition (optional).
- **WorkflowInstance** — id (unique instance ID), workflow_id, root_task_id or batch_id, status, current_node_instance_id, created_at.
- **NodeInstance** — id (unique instance ID), workflow_instance_id, node_id, status, task_id (if manual/form/review), started_at, completed_at.
- **WorkQueue** — id, name, workflow_id (optional), node_id (optional), assigned_role_or_rule (e.g. “reviewer”, “manager”), project_id.
- **WorkQueueItem** — id, work_queue_id, task_id, node_instance_id, assigned_to_user_id (nullable), status (pending | assigned | claimed | completed), created_at.

Tasks and Annotations stay as in the PRD; they are linked to **NodeInstance** (and thus to a node and workflow instance) when the task is part of a workflow run.

---

## 5. Dummy Data: 50 Indian Users with Hierarchy

For development and demos we use **50 Indian users** with a clear hierarchy:

- **Roles:** Admin (1), Ops/Manager (e.g. 5), Reviewer/QA (e.g. 10), Annotator/Rater (e.g. 34). Exact counts can vary.
- **Hierarchy:** e.g. Admin → Ops Leads → Ops → Reviewers → Annotators. Each user can have a **reports_to** (parent) and **role**.
- **Names:** Indian names (e.g. Priya Sharma, Raj Patel, Amit Kumar, etc.) — 50 distinct names.
- **Usage:** Work queues can be assigned by **role** (e.g. all Reviewers) or by **hierarchy** (e.g. tasks for “reportees of this manager”). Admin sees all; others see by assignment/role/hierarchy.

A separate **Dummy_Data_50_Indian_Users.md** (or CSV/JSON) can list: user_id, full_name, email, role, reports_to_user_id, so that the system can seed and filter correctly.

---

## 6. Task Tab: Filters and Sorting

The **Tasks** tab (for any user with task access) shows tasks relevant to them. We support:

- **Filters:** status, workflow (name/id), node type, date range, assignee, priority, tags (if applicable).
- **Sorting:** created_at, updated_at, due date, priority, status.
- **Data shown:** Only fields the user is allowed to see (asset link, form response, review outcome, etc.). Admin sees full data; others see only their assigned tasks’ data.

---

## 7. What We Are Building (Summary)

- **Workflows** as directed graphs of **nodes** and **edges**, with **unique node IDs** and **unique instance IDs** per run.
- **Node types:** form (annotation/labeling UI), review, api_call, db_update, manual — with manual/review nodes feeding **work queues**.
- **Child workflows** linkable from a node; completion in sequence.
- **Annotation flow:** Upload file → form node (add attributes) → submit → review node → manager/reviewer queue → reviewer UI → approve/reject → next nodes.
- **Data visibility:** Admin sees all; other users see only their assigned/own task data.
- **Dummy data:** 50 Indian users with hierarchy for testing and demos.
- **Task tab:** One place for all tasks with filters and sorting, respecting visibility.

This design aligns with the PRD’s pipelines, stages, task UI, queueing, and review flows while extending to configurable graph-based workflows and explicit work queues.
