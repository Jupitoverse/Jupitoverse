# Upload to GitHub — Jupitoverse/Data-Annotation

Push this **AI Project** folder to: **https://github.com/Jupitoverse/Data-Annotation.git**

## Easiest: run the batch file

Double-click **`push_to_github.bat`** in this folder. It will:

1. Add all files  
2. Commit  
3. Set remote to `https://github.com/Jupitoverse/Data-Annotation.git`  
4. Push to `main`

When GitHub asks for a password, use a **Personal Access Token** (not your account password): [Create a token](https://github.com/settings/tokens).

---

## Manual steps (terminal)

### 1. Open a terminal in the AI Project folder

```powershell
cd "C:\Users\abhisha3\Desktop\Projects\Perosnal\AI Project"
```

### 2. Add, commit, add remote, push

```powershell
git add .
git commit -m "Data Annotation Platform: Planning, V3 demo, batch scripts, presentation"
git remote remove origin
git remote add origin https://github.com/Jupitoverse/Data-Annotation.git
git branch -M main
git push -u origin main
```

### 3. Authentication

- **HTTPS:** Use a **Personal Access Token** as the password when prompted.
- **SSH:** `git remote add origin git@github.com:Jupitoverse/Data-Annotation.git`

---

After push, the repo will contain: Planning/, V3/ (demo app), Presentation_Data_Annotation_Platform.md, first_time_setup.bat, start.bat, push_to_github.bat, PRD PDF, .gitignore.
