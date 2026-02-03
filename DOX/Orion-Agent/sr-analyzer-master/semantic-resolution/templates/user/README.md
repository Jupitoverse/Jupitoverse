# 👤 User Templates

> **User Portal HTML Templates**

---

## 📁 Structure

```
user/
├── README.md
├── feedback_main.html      # Main user interface (2979 lines)
└── my_srs.html             # User's assigned SRs (350 lines)
```

---

## 📄 Templates

### `feedback_main.html`

The main user interface with comprehensive features:

**Search Section**
- SR ID search box with autocomplete
- Quick search button
- Recent searches

**SR Details Panel**
- SR ID, Priority, Application
- Description and Notes
- Business day age
- Status indicator

**AI Workaround Panel**
- AI-generated workaround
- Java Error detection indicator
- Confidence level (HIGH/MEDIUM/LOW)
- Assigned team member

**Similar SRs Panel**
- Top 10 similar historical SRs
- Similarity percentage
- Quick view workarounds

**Feedback Section**
- Voting buttons (👍 Helpful / 👎 Not Helpful)
- Correction text area
- Submit feedback button

**Known Workarounds**
- Integration with json_workaround module
- Quick lookup by category

**User Availability**
- Set availability percentage
- Half-day/Full-day options
- Out-of-office reasons

### `my_srs.html`

User's assigned SRs dashboard:
- List of SRs assigned to logged-in user
- Priority and age indicators
- Quick actions (view, feedback)
- Filter by status

---

## 🔗 Related

- [templates/README.md](../README.md) - Templates module
- [app/routes/user.py](../../app/routes/user.py) - User routes

---

*Part of SR-Analyzer Templates Module*
