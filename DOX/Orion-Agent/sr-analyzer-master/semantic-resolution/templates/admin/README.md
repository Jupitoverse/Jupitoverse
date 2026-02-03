# 🔐 Admin Templates

> **Admin Portal HTML Templates**

---

## 📁 Structure

```
admin/
├── README.md
├── admin_upload.html       # Main upload page
├── admin_remove_sr.html    # SR removal page
└── today_upload.html       # Today's upload view
```

---

## 📄 Templates

### `admin_upload.html`

Main admin dashboard with:

**Upload Section**
- Drag-and-drop file upload zone
- File type validation (.xls, .xlsx)
- Upload button
- Progress bar with percentage

**Processing Status**
- Real-time status updates
- Step indicators (Analyzing, RAG, Merging)
- Error display

**Statistics Dashboard**
- Historical SR count
- User corrections count
- Upload count
- LLM usage stats (tokens, cost)

**Recent Reports**
- List of processed files
- Download links
- Processing timestamps

### `admin_remove_sr.html`

SR removal interface:
- SR ID input
- Confirmation dialog
- Removal from ChromaDB

### `today_upload.html`

Today's upload management:
- List of today's processed files
- Status indicators (success/failed)
- Quick actions:
  - Download report
  - Reprocess
  - View details

---

## 🔗 Related

- [templates/README.md](../README.md) - Templates module
- [app/routes/admin.py](../../app/routes/admin.py) - Admin routes

---

*Part of SR-Analyzer Templates Module*
