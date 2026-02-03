# Bulk Handling Backend Implementation Guide

## Overview
The Bulk Handling feature now has a fully functional backend that integrates with the OSO Orion Comcast API endpoints.

---

## 🔧 Backend Implementation

### Files Modified/Created

1. **`backend/routes/bulk_handling.py`** - Updated with actual API implementations
2. **`templates/bulk_handling.html`** - Updated frontend with bearer token input and proper data parsing

---

## 🚀 API Endpoints

### Base URL
All endpoints are under: `http://localhost:5001/api/bulk-handling`

### Implemented Operations

#### 1. **B2: Bulk Force Complete**
- **Endpoint:** `POST /force-complete/execute`
- **Purpose:** Force complete stuck or pending orders
- **Required Input:**
  ```json
  {
    "bearer_token": "YOUR_BEARER_TOKEN",
    "items": [
      {
        "plan_id": "0F30089DABAC4A79A50EF9C8C87F45611737061897",
        "activity_id": "99A1C7B722584BC5A1617007D03015E2",
        "project_id": "Project1449179"
      }
    ]
  }
  ```
- **OSO API:** `https://oso.orion.comcast.com/frontend-services-ws-war/servicepoint/updateActivityStatus/{project_id}/{plan_id}/{activity_id}/Completed`

#### 2. **B3: Bulk Re-execute (Rework)**
- **Endpoint:** `POST /re-execute/execute`
- **Purpose:** Re-execute/rework activities
- **Required Input:**
  ```json
  {
    "bearer_token": "YOUR_BEARER_TOKEN",
    "items": [
      {
        "plan_id": "0F30089DABAC4A79A50EF9C8C87F45611737061897",
        "activity_id": "99A1C7B722584BC5A1617007D03015E2"
      }
    ]
  }
  ```
- **OSO API:** `https://oso.orion.comcast.com/frontend-services-ws-war/servicepoint/reworkActivity/{plan_id}/{activity_id}`

#### 3. **B5: Complete Stuck Activity**
- **Endpoint:** `POST /stuck-activity/complete`
- **Purpose:** Complete activities stuck in processing state
- **Required Input:**
  ```json
  {
    "bearer_token": "YOUR_BEARER_TOKEN",
    "items": [
      {
        "plan_id": "0F30089DABAC4A79A50EF9C8C87F45611737061897",
        "activity_id": "99A1C7B722584BC5A1617007D03015E2",
        "project_id": "Project1449179"
      }
    ]
  }
  ```
- **OSO API:** Same as Force Complete

---

## 📊 Response Format

All endpoints return a consistent response format:

### Success Response
```json
{
  "success": true,
  "total": 3,
  "successful": 2,
  "failed": 1,
  "message": "Bulk Force Complete: 2 successful, 1 failed",
  "results": [
    {
      "success": true,
      "plan_id": "0F30089DABAC...",
      "activity_id": "99A1C7B722...",
      "project_id": "Project1449179",
      "message": "Successfully completed"
    },
    {
      "success": false,
      "plan_id": "F9FC0070A02...",
      "activity_id": "A70327A634...",
      "error": "Forbidden: Permission denied"
    }
  ]
}
```

### Error Response
```json
{
  "success": false,
  "error": "Bearer token is required"
}
```

---

## 🎯 Frontend Usage

### 1. Enter Bearer Token
At the top of the Bulk Handling page, enter your bearer token:
```
PFVFTT5LPTxrZXk+LnN5c3RlbS5lbnYuZW5jcnlwdGlvbi4wO0M9MTc0NTM4NDg4MzA1NztNPVh9Mm5JeXsweTZ1YUg5Zzd5UmJZelAxY1VjSVgzUWI0Y2VYR0JCRUpFZUxqNkpJcnR4N2hETE9Zc0k0OHJBVTcwOzwvVUVNPg==
```

### 2. Enter IDs in Correct Format

#### For Bulk Force Complete / Complete Stuck Activity:
```
plan_id1, activity_id1, project_id1
plan_id2, activity_id2, project_id2
plan_id3, activity_id3, project_id3

Example:
0F30089DABAC4A79A50EF9C8C87F45611737061897, 99A1C7B722584BC5A1617007D03015E2, Project1449179
F9FC0070A02C4387AAABF618FA1506311737065038, A70327A634EC48238035F813E574EC21, Project323863
```

#### For Bulk Re-execute:
```
plan_id1, activity_id1
plan_id2, activity_id2
plan_id3, activity_id3

Example:
0F30089DABAC4A79A50EF9C8C87F45611737061897, 99A1C7B722584BC5A1617007D03015E2
F9FC0070A02C4387AAABF618FA1506311737065038, A70327A634EC48238035F813E574EC21
```

### 3. Submit
- Click Submit button
- Confirm the operation (popup shows count)
- View results with success/failure details

---

## 🔍 Backend Features

### 1. **Parallel Execution**
Uses ThreadPoolExecutor to process multiple items simultaneously (max 10 concurrent workers)

### 2. **Error Handling**
- Validates bearer token presence
- Handles API errors (200, 403, other status codes)
- Catches and reports network/timeout errors
- Returns detailed success/failure for each item

### 3. **Detailed Results**
Each result includes:
- Success status
- Plan ID, Activity ID, Project ID (if applicable)
- Success message or error description

### 4. **Timeout Protection**
30-second timeout per API request to prevent hanging

---

## 🔐 Security Notes

### Bearer Token
- **NEVER** commit bearer tokens to version control
- Tokens should be refreshed regularly
- Current format: Base64 encoded UEM token
- Example: `PFVFTT5LPTxrZXk+...`

### Production Considerations
1. Store bearer token in environment variables or secure vault
2. Implement token refresh mechanism
3. Add rate limiting to prevent API abuse
4. Log all operations for audit trail

---

## 📝 To Be Implemented

The following operations still need base URLs and implementation:

### B1: Bulk Retry
- **Status:** ❌ Not implemented (missing base URL)
- **Purpose:** Retry failed orders/activities

### B4: Bulk Resolve Error
- **Status:** ❌ Not implemented (missing base URL)
- **Purpose:** Resolve errors in bulk

### B6: Bulk Flag Release
- **Status:** ⚠️ Placeholder exists
- **Purpose:** Set flags for multiple projects
- **Needs:** Base URL and implementation logic

---

## 🧪 Testing

### Manual Testing
1. Navigate to Bulk Handling tab
2. Enter valid bearer token
3. Enter test IDs in correct format
4. Submit and verify results

### API Testing (using curl)
```bash
curl -X POST http://localhost:5001/api/bulk-handling/force-complete/execute \
  -H "Content-Type: application/json" \
  -d '{
    "bearer_token": "YOUR_TOKEN",
    "items": [
      {
        "plan_id": "TEST_PLAN_ID",
        "activity_id": "TEST_ACTIVITY_ID",
        "project_id": "TEST_PROJECT_ID"
      }
    ]
  }'
```

---

## 📚 References

### OSO Orion API Endpoints
- **Base URL:** `https://oso.orion.comcast.com/frontend-services-ws-war/servicepoint/`
- **Update Activity Status:** `updateActivityStatus/{project_id}/{plan_id}/{activity_id}/{status}`
- **Rework Activity:** `reworkActivity/{plan_id}/{activity_id}`

### Documentation Files
- `bulk_handling.md` - Original requirements and Python scripts
- `templates/bulk_handling.html` - Frontend implementation
- `backend/routes/bulk_handling.py` - Backend implementation

---

## 🎉 Usage Example

**Scenario:** Force complete 3 stuck activities

1. **Open** Bulk Handling page in browser
2. **Enter** bearer token in the top field
3. **Navigate** to "Bulk Force Complete" tab
4. **Paste** the following:
   ```
   0F30089DABAC4A79A50EF9C8C87F45611737061897, 99A1C7B722584BC5A1617007D03015E2, Project1449179
   F9FC0070A02C4387AAABF618FA1506311737065038, A70327A634EC48238035F813E574EC21, Project323863
   673932C6BDBF4E6BA4C4E73760CD8ACC1737063183, 7254937575D546F5B55676FAA6AE00D1, Project830199
   ```
5. **Click** Submit
6. **Confirm** when prompted (shows "3 items")
7. **View** results showing:
   - Total: 3
   - Successful: X
   - Failed: Y
   - Detailed list of each item's status

---

**Last Updated:** January 20, 2025  
**Version:** 1.0  
**Backend Status:** ✅ Functional for B2, B3, B5



