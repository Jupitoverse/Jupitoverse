# 🚀 Orionverse Quick Reference

**Version**: 3.2 | **Last Updated**: November 4, 2025

---

## 📖 Essential Files (Read These First!)

| File | Purpose | When to Read |
|------|---------|--------------|
| **README.md** | Project overview & features | First time setup |
| **REQUIREMENTS.md** | Dependencies & installation | Setting up environment |
| **FILE_STRUCTURE.md** | Complete file guide | Finding specific files |
| **PROMPT_HISTORY.md** | Complete project history | Understanding context |
| **AVD_DEPLOYMENT_GUIDE.md** | AVD deployment steps | Deploying to AVD |

---

## 🏃 Quick Start (Local Development)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start backend (Windows)
scripts\START_BACKEND.bat

# 3. Open in browser
http://localhost:5001
```

---

## 🌐 Quick Start (Network Deployment)

```bash
# 1. Start network backend
scripts\START_NETWORK_BACKEND.bat

# 2. Open in browser from any machine
http://<your-machine-ip>:5001
```

See: `AVD_DEPLOYMENT_GUIDE.md` for complete instructions

---

## 📂 Where to Find Things

| Need to... | Look in... |
|------------|------------|
| Start the server | `scripts/START_BACKEND.bat` |
| Read documentation | `docs/` folder |
| Check project history | `PROMPT_HISTORY.md` |
| See all files explained | `FILE_STRUCTURE.md` |
| Find dependencies | `REQUIREMENTS.md` |
| Modify frontend | `static/js/` and `templates/` |
| Add API endpoints | `backend/routes/` |
| Test API | `scripts/test_api.html` |
| Setup AVD | `AVD_DEPLOYMENT_GUIDE.md` |

---

## ✨ Key Features

- **Search Anything**: Multi-source search (SR, Defects, Workarounds)
- **Bulk Handling**: 6 bulk operations (Retry, Force Complete, etc.)
- **Abbreviations**: 120+ abbreviations with search
- **Welcome Kit**: Apps & DB credentials for new joiners
- **Workarounds**: Collaborative workaround system

---

## 🆘 Common Issues

### Backend not starting?
```bash
# Check if port 5001 is in use
netstat -ano | findstr :5001

# Kill process if needed
taskkill /PID <PID> /F
```

### Search not working?
1. Check if backend is running
2. Open browser console (F12)
3. Check for API errors
4. Verify `backend/data/sr_data.json` exists

### Tab switching not working?
1. Clear browser cache
2. Hard refresh (Ctrl+F5)
3. Check browser console for errors

---

## 📚 Documentation Map

### Getting Started
- `README.md` - Overview
- `REQUIREMENTS.md` - Setup requirements
- `docs/QUICK_START.md` - Quick start guide

### Features
- `docs/SEARCH_ENGINE_GUIDE.md` - Search feature
- `docs/BULK_HANDLING_GUIDE.md` - Bulk operations
- `docs/WORKAROUND_SETUP_GUIDE.md` - Workaround system

### Deployment
- `AVD_DEPLOYMENT_GUIDE.md` - AVD deployment
- `docs/NETWORK_DEPLOYMENT_GUIDE.md` - Network setup
- `docs/DEPLOYMENT_CHECKLIST.md` - Deployment checklist

### Development
- `FILE_STRUCTURE.md` - File structure
- `PROMPT_HISTORY.md` - Project history
- `docs/DEVELOPER_GUIDE.md` - Developer docs
- `docs/ARCHITECTURE.md` - System architecture

---

## 🔧 Useful Commands

```bash
# Start local backend
scripts\START_BACKEND.bat

# Start network backend
scripts\START_NETWORK_BACKEND.bat

# Test network access
scripts\test_network_access.ps1

# Setup AVD (automated)
scripts\setup_avd.ps1

# Convert Excel to JSON
python scripts\convert_excel.py
```

---

## 🎯 Current Capabilities

✅ Multi-source search (SR, Defects, Workarounds)  
✅ 6 bulk operations with confirmation popups  
✅ 120+ abbreviations with real-time search  
✅ Welcome Kit with apps and DB credentials  
✅ Collaborative workaround system  
✅ Dark purple theme UI  
✅ Network deployment ready  
✅ AVD deployment ready  
✅ Clean file structure  

---

## 💡 Pro Tips

1. **Use Ctrl+P in VS Code** to quickly find files
2. **Check browser console (F12)** for frontend errors
3. **Check terminal** for backend errors
4. **Read FILE_STRUCTURE.md** to understand file organization
5. **Use START_BACKEND.bat** for quick server start
6. **Check docs/ folder** for detailed feature documentation

---

## 📞 Need Help?

1. Check `docs/PROJECT_CONTEXT.md` for complete history
2. Read `FILE_STRUCTURE.md` for file locations
3. See `REQUIREMENTS.md` for dependency issues
4. Check `docs/` folder for feature-specific guides
5. Contact Orion team for database credentials

---

**Quick Links:**
- Backend: http://localhost:5001
- API Docs: See `docs/DEVELOPER_GUIDE.md`
- Deployment: See `AVD_DEPLOYMENT_GUIDE.md`

---

*This is a quick reference. For detailed information, see the individual documents listed above.*


