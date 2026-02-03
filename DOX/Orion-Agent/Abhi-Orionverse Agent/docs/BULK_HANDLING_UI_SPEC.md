# Bulk Handling - Updated UI Specification

**Date**: November 4, 2025  
**Version**: 3.2 (Simplified)

---

## Overview

The Bulk Handling UI has been redesigned with a simplified, cleaner interface. Each operation now has:
- **One large text box** for input (comma-separated or line-separated)
- **Line counter** showing number of items
- **Submit button** that triggers confirmation popup
- **Results display** showing operation outcome

---

## Operations

### B1: Bulk Retry
**Input Fields**:
- Large text box for: `activity_ids, plan_ids, error_id`

**Backend Endpoint**: `POST /api/bulk-handling/retry/execute`

**Request Format**:
```json
{
  "ids": ["12345", "67890", "11223"]
}
```

**Response Format**:
```json
{
  "success": true,
  "total": 3,
  "successful": 3,
  "failed": 0,
  "message": "Bulk Retry: 3 successful, 0 failed"
}
```

**Result Display**: "✅ Success: 3 activities retried"

---

### B2: Bulk Force Complete
**Input Fields**:
- Large text box for: `activity_ids, plan_ids, error_id`

**Backend Endpoint**: `POST /api/bulk-handling/force-complete/execute`

**Request Format**:
```json
{
  "ids": ["12345", "67890", "11223"]
}
```

**Response Format**:
```json
{
  "success": true,
  "total": 3,
  "successful": 3,
  "failed": 0,
  "message": "Bulk Force Complete: 3 successful, 0 failed"
}
```

**Result Display**: "✅ Success: 3 activities force completed"

---

### B3: Bulk Re-execute
**Input Fields**:
- Large text box for: `activity_ids, plan_ids`

**Backend Endpoint**: `POST /api/bulk-handling/re-execute/execute`

**Request Format**:
```json
{
  "ids": ["12345", "67890"]
}
```

**Response Format**:
```json
{
  "success": true,
  "total": 2,
  "successful": 2,
  "failed": 0,
  "message": "Bulk Re-execute: 2 successful, 0 failed"
}
```

**Result Display**: "✅ Success: 2 activities re-executed"

---

### B4: Bulk Resolve Error
**Input Fields**:
- Large text box for: `activity_ids, plan_ids, error_id`

**Backend Endpoint**: `POST /api/bulk-handling/resolve-error/execute`

**Request Format**:
```json
{
  "ids": ["12345", "67890", "11223"]
}
```

**Response Format**:
```json
{
  "success": true,
  "total": 3,
  "successful": 3,
  "failed": 0,
  "message": "Bulk Resolve Error: 3 successful, 0 failed"
}
```

**Result Display**: "✅ Success: 3 errors resolved"

---

### B5: Complete Stuck Activity
**Input Fields**:
- Large text box for: `activity_ids, plan_ids`

**Backend Endpoint**: `POST /api/bulk-handling/stuck-activity/complete`

**Request Format**:
```json
{
  "ids": ["12345", "67890"]
}
```

**Response Format**:
```json
{
  "success": true,
  "total": 2,
  "successful": 2,
  "failed": 0,
  "message": "Complete Stuck Activity: 2 successful, 0 failed"
}
```

**Result Display**: "✅ Success: 2 stuck activities completed"

---

### B6: Bulk Flag Release
**Input Fields**:
- Small text box for: `attribute_name`
- Small text box for: `flag` value
- Large text box for: `project_ids` (multi-line)

**Backend Endpoint**: `POST /api/bulk-handling/flag-release/execute`

**Request Format**:
```json
{
  "project_ids": ["PROJECT_001", "PROJECT_002", "PROJECT_003"],
  "attribute_name": "release_flag",
  "flag_value": "approved"
}
```

**Response Format**:
```json
{
  "success": true,
  "total": 3,
  "successful": 3,
  "failed": 0,
  "message": "Bulk Flag Release: 3 successful, 0 failed"
}
```

**Result Display**: "✅ Success: 3 projects flagged"

---

## UI Features

### Line Counter
- Displays in real-time as user types
- Shows number of valid IDs entered
- Format: "Lines: **N**"
- Green color with subtle background

### Confirmation Popup
- Appears when Submit is clicked
- Shows operation details
- Displays line count: "Are you sure you want to [action] **N** item(s)?"
- Yes/No buttons
- Modal overlay with blur effect

### Results Display
- Success: Green with checkmark "✅ Success: N activities [action]"
- Warning: Yellow/orange for partial failures "⚠️ N items failed"
- Error: Red with X "❌ Error: [message]"
- Info: Blue for processing "⏳ Processing..."

### Input Format Examples

**Comma-separated**:
```
12345, 67890, 11223, 44556
```

**Line-separated**:
```
12345
67890
11223
44556
```

**Mixed**:
```
12345, 67890
11223
44556, 77889
```

All formats are automatically parsed and counted.

---

## Backend Integration Points

### Where to Add Your Code

Each endpoint in `backend/routes/bulk_handling.py` has a marked section:

```python
# ============================================
# TODO: Add your Python code here for B1
# ============================================
```

Replace the placeholder implementation with your actual code.

### Expected Variables Available

For B1-B5:
- `ids` - List of parsed IDs from input

For B6:
- `project_ids` - List of project IDs
- `attribute_name` - String attribute name
- `flag_value` - String flag value

### Expected Return Format

Your code should set these variables:
- `successful` - Integer count of successful operations
- `failed` - Integer count of failed operations

The endpoint will automatically format the response.

### Error Handling

All endpoints have try-catch blocks. Your code can:
- Raise exceptions (will be caught and returned as error)
- Return early with custom response
- Modify the response JSON as needed

---

## Testing

### Using curl

**Test B1 - Bulk Retry**:
```bash
curl -X POST http://localhost:5001/api/bulk-handling/retry/execute \
  -H "Content-Type: application/json" \
  -d '{"ids": ["12345", "67890"]}'
```

**Test B6 - Bulk Flag Release**:
```bash
curl -X POST http://localhost:5001/api/bulk-handling/flag-release/execute \
  -H "Content-Type: application/json" \
  -d '{
    "project_ids": ["PROJECT_001", "PROJECT_002"],
    "attribute_name": "release_flag",
    "flag_value": "approved"
  }'
```

### Health Check

```bash
curl http://localhost:5001/api/bulk-handling/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "bulk_handling",
  "endpoints": [
    "B1: /retry/execute",
    "B2: /force-complete/execute",
    "B3: /re-execute/execute",
    "B4: /resolve-error/execute",
    "B5: /stuck-activity/complete",
    "B6: /flag-release/execute"
  ]
}
```

---

## File Locations

- **Frontend Template**: `templates/bulk_handling.html`
- **Backend Routes**: `backend/routes/bulk_handling.py`
- **Main App**: `backend/app.py` (blueprint already registered)

---

## Next Steps

1. ✅ UI is complete and ready
2. ✅ Backend endpoints are set up with placeholders
3. ⏳ Add your Python code to each endpoint
4. ✅ Test each operation
5. ✅ Deploy to production

---

## Notes

- All text boxes support both comma and newline separation
- Line counter updates in real-time
- Confirmation popup prevents accidental submissions
- Results are displayed with clear success/failure counts
- Backend is ready for your custom Python implementation

---

**Status**: Ready for backend implementation  
**UI Status**: Complete ✅  
**Backend Status**: Awaiting your Python code ⏳

