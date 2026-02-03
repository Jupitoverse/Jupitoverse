# Bulk Re-execute - Streamlit UI Quick Start Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_streamlit.txt
```

Or install individually:
```bash
pip install streamlit requests pandas
```

### 2. Run the Application

```bash
streamlit run Rework_Streamlit.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 📋 Features

### ✅ What's Included:

1. **Bearer Token Input**
   - Secure password field for authentication token
   - Token is masked for security

2. **Multi-line Input Box**
   - Enter activity_id and plan_id pairs
   - Format: `activity_id, plan_id` (one per line)
   - Real-time line counter shows number of activities

3. **Line Counter**
   - Displays total number of activities to be processed
   - Updates automatically as you type

4. **Confirmation Dialog**
   - Shows: "Are you sure to rework X activities?"
   - Displays estimated execution time
   - Yes/No buttons for confirmation

5. **5-Second Delay**
   - Automatic 5-second pause between each API call
   - Countdown timer displayed
   - Prevents production overload

6. **Progress Tracking**
   - Real-time progress bar
   - Current activity being processed
   - Success/failure status for each call

7. **Summary Report**
   - Total processed count
   - Success/failure metrics
   - Detailed results table
   - Download results as CSV

---

## 📝 How to Use

### Step 1: Enter Bearer Token
```
Paste your authentication bearer token in the password field
```

### Step 2: Enter Activity & Plan IDs
```
Format: activity_id, plan_id (one per line)

Example:
99A1C7B722584BC5A1617007D03015E2, 0F30089DABAC4A79A50EF9C8C87F45611737061897
A70327A634EC48238035F813E574EC21, F9FC0070A02C4387AAABF618FA1506311737065038
7254937575D546F5B55676FAA6E00D1, 673932C6BDBF4E6BA4C4E73760CD8ACC1737063183
```

### Step 3: Review Line Count
```
The line counter will show: "Total Lines: 3 activities to be processed"
```

### Step 4: Click Submit
```
Click the "Submit" button
```

### Step 5: Confirm Execution
```
Confirmation dialog appears:
"Are you sure you want to rework 3 activities?"
Estimated time: 0 minutes 15 seconds

Click "Yes, Proceed" to continue or "Cancel" to abort
```

### Step 6: Monitor Progress
```
Watch real-time execution:
- Progress bar shows completion percentage
- Each activity's success/failure is displayed
- 5-second countdown between calls
```

### Step 7: Review Summary
```
After completion:
- View success/failure metrics
- Check detailed results table
- Download CSV report if needed
```

---

## 🎨 UI Features

### Color-Coded Status:
- ✅ **Green** = Success
- ❌ **Red** = Error/Failure
- ⚠️ **Yellow** = Warning/Info
- 🔵 **Blue** = In Progress

### Real-time Updates:
- Progress bar updates with each call
- Status messages update in real-time
- Countdown timer for delays
- Live result logging

### Responsive Design:
- Works on desktop and tablet
- Clean, professional interface
- Easy-to-read typography
- Intuitive layout

---

## 🔧 Configuration

### API Endpoint:
```python
base_url = "https://oso.orion.comcast.com/frontend-services-ws-war/servicepoint/reworkActivity"
```

### Delay Between Calls:
```python
# Default: 5 seconds
# To change, modify line 267 in Rework_Streamlit.py:
for remaining in range(5, 0, -1):  # Change 5 to desired seconds
```

### Timeout:
```python
# Default: 30 seconds per API call
# To change, modify line 123 in Rework_Streamlit.py:
response = requests.get(url, headers=headers, timeout=30)  # Change 30
```

---

## 📊 Output Format

### CSV Export Columns:
1. `status` - success or error
2. `plan_id` - Plan ID
3. `activity_id` - Activity ID
4. `status_code` - HTTP status code
5. `message` - Success/error message

### Example CSV:
```csv
status,plan_id,activity_id,status_code,message
success,0F30089DABAC4A79A50EF9C8C87F45611737061897,99A1C7B722584BC5A1617007D03015E2,200,Successfully executed
error,F9FC0070A02C4387AAABF618FA1506311737065038,A70327A634EC48238035F813E574EC21,403,Forbidden: No permission to access this resource
```

---

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution**: Install required packages
```bash
pip install streamlit requests pandas
```

### Issue: "Port already in use"
**Solution**: Use a different port
```bash
streamlit run Rework_Streamlit.py --server.port 8502
```

### Issue: "Connection timeout"
**Solution**: Increase timeout in code (line 123)
```python
response = requests.get(url, headers=headers, timeout=60)  # Increase to 60 seconds
```

### Issue: "403 Forbidden"
**Solution**: 
- Check if bearer token is correct
- Verify token hasn't expired
- Ensure you have permission to access the resource

### Issue: "Invalid format warning"
**Solution**: Ensure input format is correct
```
Correct: activity_id, plan_id
Wrong: activity_id,plan_id,extra_value
Wrong: activity_id plan_id
```

---

## 🔒 Security Notes

1. **Bearer Token**: Never share your bearer token
2. **Password Field**: Token is masked in the UI
3. **Session State**: Token is stored only in browser session
4. **No Logging**: Token is not logged to console or files

---

## 📈 Performance Tips

1. **Batch Size**: Process 50-100 activities at a time for optimal performance
2. **Delay**: Keep 5-second delay to avoid overloading production
3. **Timeout**: Increase timeout for slow network connections
4. **Browser**: Use Chrome or Firefox for best experience

---

## 🎯 Advanced Usage

### Running on Network:
```bash
streamlit run Rework_Streamlit.py --server.address 0.0.0.0 --server.port 8501
```

### Running in Background:
```bash
# Linux/Mac
nohup streamlit run Rework_Streamlit.py &

# Windows
start /B streamlit run Rework_Streamlit.py
```

### Custom Theme:
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#1f77b4"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
textColor="#262730"
font="sans serif"
```

---

## 📞 Support

For issues or questions:
- **Email**: abhisha3@amdocs.com
- **Project**: Orion Bulk Operations

---

## 📝 Changelog

### Version 1.0 (November 2025)
- Initial release
- Bearer token authentication
- Multi-line input with line counter
- Confirmation dialog
- 5-second delay between calls
- Progress tracking
- Summary report with CSV export

---

**Last Updated**: November 11, 2025  
**Author**: Abhishek Agrahari


