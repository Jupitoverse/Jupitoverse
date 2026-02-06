# Data Annotation Platform

Planning, demo app, and presentation materials for the Data Annotation Platform (PRD Addendum v2.0).

## Run the demo (no Docker)

1. **First time:** Double-click **`first_time_setup.bat`** to install Python dependencies.
2. **Start app:** Double-click **`start.bat`**.
3. Open **http://localhost:8000** in your browser.  
   Login: **abhi@demo.com** / **admin123** (admin) or see [V3/README.md](V3/README.md) for other demo users.

## Contents

- **Planning/** — Approach (No-LLM vs With-LLM), implementation plan, tech stack, resources, prompts.
- **docs/** — **Developer User Guide** (workflow model, node types, work queue, data visibility), **PRD Validation Checklist**, **Dummy Data: 50 Indian Users** (hierarchy for demos).
- **V3/** — Runnable demo: FastAPI + SQLite, N8n/Netflix-style dark UI. See [V3/README.md](V3/README.md).
- **presentation/** — Phase 1 deck: run `run_generate_ppt.bat` or `python generate_phase1_presentation.py` to create **Phase1_Data_Annotation_Platform.pptx** (architecture, data model, workflow & visibility, infra, deployment, monitoring). Text version: **Phase1_Presentation_Content.txt**.
- **Presentation_Data_Annotation_Platform.md** — Stakeholder presentation and discovery questions.
- **first_time_setup.bat** — Installs requirements (run once).
- **start.bat** — Starts the app locally.

## Upload to GitHub

**Easiest:** Double-click **`push_to_github.bat`**. It will add, commit, set remote, and push to **https://github.com/Jupitoverse/Data-Annotation.git**. When prompted for password, use a [Personal Access Token](https://github.com/settings/tokens).

Or see **[GITHUB_UPLOAD.md](GITHUB_UPLOAD.md)** for manual commands.
