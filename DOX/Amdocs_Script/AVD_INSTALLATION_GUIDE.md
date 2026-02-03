# AVD Installation Guide - Bulk Re-execute Streamlit App

## 🚀 Quick Installation (No Build Tools Required)

### ✅ **FIXED VERSION - No pandas/pyarrow dependency**

---

## 📋 Step-by-Step Installation

### **Step 1: Install Python Dependencies**

```powershell
# Install only streamlit and requests (NO pandas!)
pip install streamlit==1.28.0 requests==2.31.0
```

**OR** use the requirements file:

```powershell
pip install -r requirements_streamlit.txt
```

---

### **Step 2: Verify Installation**

```powershell
# Check if streamlit is installed
streamlit --version

# Should show: Streamlit, version 1.28.0
```

---

### **Step 3: Run the Application**

```powershell
# Navigate to the script directory
cd "C:\Users\aagrah262\OneDrive - Comcast\Desktop\Automation"

# Run the app
streamlit run Rework_Streamlit.py
```

---

## 🔧 If You Still Get Errors

### **Error: "No module named 'streamlit'"**

**Solution:**
```powershell
python -m pip install streamlit==1.28.0 requests==2.31.0
```

---

### **Error: "pip is not recognized"**

**Solution:**
```powershell
# Use full path to pip
C:\Python314\Scripts\pip.exe install streamlit==1.28.0 requests==2.31.0
```

---

### **Error: "Access denied" or "Permission error"**

**Solution:**
```powershell
# Install for current user only
pip install --user streamlit==1.28.0 requests==2.31.0
```

---

### **Error: "Certificate verification failed"**

**Solution:**
```powershell
# Disable SSL verification (corporate proxy issue)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org streamlit==1.28.0 requests==2.31.0
```

---

## 📦 What Changed?

### **Before (Had Issues):**
```
requirements_streamlit.txt:
- streamlit
- requests
- pandas  ❌ (requires pyarrow, which needs C++ build tools)
```

### **After (Fixed):**
```
requirements_streamlit.txt:
- streamlit==1.28.0  ✅
- requests==2.31.0   ✅
- NO pandas!         ✅
```

### **Code Changes:**
- Removed `import pandas as pd`
- Added `import csv` and `from io import StringIO`
- Replaced `pd.DataFrame()` with HTML table
- Replaced `df.to_csv()` with `csv.DictWriter()`
- All functionality remains the same!

---

## ✅ Verify Everything Works

### **Test 1: Check Python Version**
```powershell
python --version
# Should show: Python 3.14.x or 3.12.x or 3.11.x
```

### **Test 2: Check Streamlit**
```powershell
streamlit hello
# Should open a demo app in browser
```

### **Test 3: Run Your App**
```powershell
streamlit run Rework_Streamlit.py
# Should open at http://localhost:8501
```

---

## 🌐 Running on Network (Optional)

If you want to access from other machines on the network:

```powershell
streamlit run Rework_Streamlit.py --server.address 0.0.0.0 --server.port 8501
```

Then access from any machine:
```
http://<your-avd-ip>:8501
```

---

## 🔥 One-Line Installation

```powershell
pip install streamlit==1.28.0 requests==2.31.0 && streamlit run Rework_Streamlit.py
```

---

## 📊 What You Get

### **Same Features, No pandas:**
✅ Bearer token input  
✅ Multi-line input with line counter  
✅ Confirmation dialog  
✅ 5-second delay between calls  
✅ Progress tracking  
✅ Color-coded results table (HTML instead of pandas)  
✅ CSV download (using Python's csv module)  
✅ Summary metrics  

---

## 🐛 Common Issues on AVD

### **Issue 1: Port 8501 already in use**
```powershell
# Use different port
streamlit run Rework_Streamlit.py --server.port 8502
```

### **Issue 2: Browser doesn't open automatically**
```powershell
# Manually open browser and go to:
http://localhost:8501
```

### **Issue 3: Streamlit keeps restarting**
```powershell
# Disable file watcher
streamlit run Rework_Streamlit.py --server.fileWatcherType none
```

---

## 💡 Pro Tips

1. **Pin Versions**: Always use specific versions (e.g., `streamlit==1.28.0`)
2. **No pandas Needed**: This app doesn't need pandas for data processing
3. **Corporate Proxy**: Use `--trusted-host` flags if behind proxy
4. **Virtual Environment**: Consider using `venv` for isolation

---

## 📞 Support

If you still face issues:

1. **Check Python version**: `python --version`
2. **Check pip version**: `pip --version`
3. **Try upgrading pip**: `python -m pip install --upgrade pip`
4. **Contact**: abhisha3@amdocs.com

---

## ✅ Success Checklist

- [ ] Python 3.11+ installed
- [ ] pip working
- [ ] streamlit==1.28.0 installed
- [ ] requests==2.31.0 installed
- [ ] NO pandas installed (not needed!)
- [ ] Rework_Streamlit.py in correct directory
- [ ] Can run: `streamlit run Rework_Streamlit.py`
- [ ] Browser opens at http://localhost:8501
- [ ] App loads without errors

---

**Last Updated**: November 11, 2025  
**Version**: 2.0 (No pandas dependency)  
**Author**: Abhishek Agrahari


