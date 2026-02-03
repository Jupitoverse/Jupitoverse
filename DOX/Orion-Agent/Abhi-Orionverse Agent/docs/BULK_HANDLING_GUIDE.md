# Bulk Handling Operations Guide

**Version**: 1.0  
**Last Updated**: November 4, 2025  
**Feature**: Bulk Operations for Order Management and Error Resolution

---

## Overview

The **Bulk Handling** feature provides a comprehensive set of tools for performing bulk operations on orders, activities, and errors in the Orionverse system. This feature is designed to streamline operations and reduce manual effort when dealing with multiple items.

---

## Features

### 1. Bulk Retry
**Purpose**: Retry failed orders or activities in bulk

**Use Cases**:
- Retry orders that failed due to temporary issues
- Reprocess activities after system recovery
- Batch retry after fixing underlying issues

**Input Types**:
- Order IDs
- SR IDs
- Customer IDs
- OSite IDs

**Required Fields**:
- IDs (comma-separated or line-separated)
- Retry reason (mandatory)

**Process**:
1. Enter IDs in the text area
2. Select input type
3. Provide retry reason
4. Click "Validate IDs" to check validity
5. Click "Execute Retry" to perform bulk retry
6. View detailed results

---

### 2. Bulk Force Complete
**Purpose**: Force complete stuck or pending orders

**Use Cases**:
- Complete orders stuck in pending state
- Force closure of orders with known issues
- Batch complete orders after manual verification

**Input Types**:
- Order IDs
- SR IDs
- Activity IDs

**Target Status Options**:
- Completed
- Closed
- Resolved

**Required Fields**:
- IDs
- Target status
- Comments (optional but recommended)

**Process**:
1. Enter IDs
2. Select input type
3. Choose target status
4. Add comments
5. Validate and execute

---

### 3. Bulk Re-execute
**Purpose**: Re-execute orders or workflows from a specific step

**Use Cases**:
- Re-run workflows from failed step
- Restart orders from beginning
- Execute from custom step after manual intervention

**Input Types**:
- Order IDs
- SR IDs
- Workflow IDs

**Re-execute Options**:
- From Beginning
- From Failed Step
- Custom Step (specify step name)

**Priority Levels**:
- Normal
- High
- Urgent

**Process**:
1. Enter IDs
2. Select re-execute point
3. Set priority
4. Validate and execute

---

### 4. Bulk Resolve Error
**Purpose**: Resolve errors in bulk for failed orders or activities

**Use Cases**:
- Auto-fix validation errors
- Skip failed steps
- Manual override for known issues
- Rollback problematic changes

**Input Types**:
- Order IDs
- SR IDs
- Error IDs

**Error Types**:
- All Errors
- Validation Errors
- Timeout Errors
- System Errors
- Data Errors

**Resolution Actions**:
- Auto Fix
- Skip Failed Step
- Manual Override
- Rollback

**Process**:
1. Enter IDs
2. Select error type
3. Choose resolution action
4. Add resolution notes
5. Validate and execute

---

### 5. Complete Stuck Activity
**Purpose**: Complete activities that are stuck in processing state

**Use Cases**:
- Complete activities stuck for > X hours
- Batch complete activities by status
- Clean up stuck activities after system issues

**Search Types**:
- Activity IDs (direct)
- Order IDs (find related activities)
- Age-Based (stuck > X hours)
- Status-Based (by activity status)

**Activity Statuses**:
- In Progress
- Pending
- Waiting
- Processing

**Completion Status Options**:
- Completed
- Completed with Errors
- Cancelled

**Process**:
1. Select search type
2. Enter search criteria
3. Click "Search Activities" to find stuck items
4. Review found activities
5. Choose completion status
6. Add comments
7. Click "Complete Activities"

---

## API Endpoints

### Bulk Retry
```
POST /api/bulk-handling/retry/validate
POST /api/bulk-handling/retry/execute
```

### Bulk Force Complete
```
POST /api/bulk-handling/force-complete/validate
POST /api/bulk-handling/force-complete/execute
```

### Bulk Re-execute
```
POST /api/bulk-handling/re-execute/validate
POST /api/bulk-handling/re-execute/execute
```

### Bulk Resolve Error
```
POST /api/bulk-handling/resolve-error/validate
POST /api/bulk-handling/resolve-error/execute
```

### Complete Stuck Activity
```
POST /api/bulk-handling/stuck-activity/search
POST /api/bulk-handling/stuck-activity/complete
```

### Health Check
```
GET /api/bulk-handling/health
```

---

## Request/Response Examples

### Validate IDs Request
```json
{
  "ids": ["12345", "67890", "11223"],
  "input_type": "order_ids"
}
```

### Validate IDs Response
```json
{
  "success": true,
  "valid_count": 3,
  "invalid_count": 0,
  "valid_ids": ["12345", "67890", "11223"],
  "invalid_ids": [],
  "message": "Validated 3 valid order_ids"
}
```

### Execute Bulk Retry Request
```json
{
  "ids": ["12345", "67890"],
  "input_type": "order_ids",
  "reason": "Retry after system recovery"
}
```

### Execute Bulk Retry Response
```json
{
  "success": true,
  "total": 2,
  "successful": 2,
  "failed": 0,
  "results": {
    "successful": [
      {
        "id": "12345",
        "status": "retry_initiated",
        "message": "Retry successfully initiated"
      },
      {
        "id": "67890",
        "status": "retry_initiated",
        "message": "Retry successfully initiated"
      }
    ],
    "failed": []
  },
  "message": "Retry completed: 2 successful, 0 failed"
}
```

### Search Stuck Activities Request
```json
{
  "search_type": "age_based",
  "age": 24,
  "ids": [],
  "status": ""
}
```

### Search Stuck Activities Response
```json
{
  "success": true,
  "found_count": 15,
  "activities": [
    {
      "activity_id": "ACT_12345",
      "order_id": "ORD_67890",
      "status": "stuck",
      "duration_hours": 48,
      "last_update": "2025-11-03 10:30:00"
    }
  ],
  "message": "Found 15 stuck activities"
}
```

---

## Input Format

### Comma-Separated
```
12345, 67890, 11223, 44556
```

### Line-Separated
```
12345
67890
11223
44556
```

### Mixed (Both work)
```
12345, 67890
11223
44556, 77889
```

---

## Best Practices

### 1. Always Validate First
- Use "Validate IDs" before executing
- Review validation results
- Fix invalid IDs before proceeding

### 2. Provide Meaningful Comments
- Add clear reasons for bulk operations
- Document any manual steps taken
- Include ticket/incident references

### 3. Start Small
- Test with a small batch first
- Verify results before processing larger batches
- Monitor system performance

### 4. Review Results
- Check success/failure counts
- Review failed items
- Take corrective action for failures

### 5. Use Appropriate Priority
- Normal: Regular batch operations
- High: Time-sensitive operations
- Urgent: Critical business impact

---

## Error Handling

### Validation Errors
- Invalid ID format
- Empty ID list
- Missing required fields

**Action**: Fix input and retry validation

### Execution Errors
- System unavailable
- Database connection issues
- Authorization failures

**Action**: Check system status, retry after resolution

### Partial Failures
- Some IDs succeed, others fail
- Mixed results in batch

**Action**: Review failed items, retry individually if needed

---

## Monitoring & Logging

### Backend Logs
All bulk operations are logged with:
- Operation type
- User ID
- Timestamp
- IDs processed
- Success/failure counts
- Error details

### Log Format
```
⚡ Executing bulk retry for 10 order_ids
   Reason: Retry after system recovery
✓ Retry completed: 9 successful, 1 failed
```

### Accessing Logs
Check backend logs at:
```
backend/logs/bulk_handling.log
```

---

## Troubleshooting

### Issue: Validation Always Fails
**Possible Causes**:
- Invalid ID format
- Backend not running
- Network connectivity issues

**Solution**:
1. Check ID format (numeric only)
2. Verify backend is running
3. Test API endpoint: `GET /api/bulk-handling/health`

### Issue: Execute Button Disabled
**Possible Causes**:
- Validation not performed
- Validation failed
- No IDs entered

**Solution**:
1. Enter valid IDs
2. Click "Validate IDs"
3. Wait for validation to complete

### Issue: Slow Performance
**Possible Causes**:
- Large batch size
- System load
- Database performance

**Solution**:
1. Reduce batch size
2. Execute during off-peak hours
3. Monitor system resources

---

## Security & Permissions

### Access Control
- Bulk operations require appropriate user permissions
- All operations are logged with user ID
- Audit trail maintained for compliance

### Authorization
- User must be authenticated
- Role-based access control (RBAC) enforced
- Sensitive operations require elevated privileges

---

## Future Enhancements

### Planned Features
- [ ] Scheduled bulk operations
- [ ] Bulk operation templates
- [ ] Export results to Excel/CSV
- [ ] Email notifications for completion
- [ ] Dry-run mode (preview without executing)
- [ ] Undo/rollback for bulk operations
- [ ] Bulk operation history and audit log
- [ ] Advanced filtering and search
- [ ] Integration with workflow engine
- [ ] Real-time progress tracking

---

## Quick Reference

| Operation | Validates | Executes | Key Feature |
|-----------|-----------|----------|-------------|
| Bulk Retry | ✓ | ✓ | Retry with reason |
| Force Complete | ✓ | ✓ | Target status selection |
| Re-execute | ✓ | ✓ | Custom step support |
| Resolve Error | ✓ | ✓ | Error type filtering |
| Complete Stuck | Search | ✓ | Age/status based search |

---

## Support

For issues or questions:
1. Check this guide
2. Review backend logs
3. Test API health endpoint
4. Contact Orionverse support team

---

**END OF BULK HANDLING GUIDE**

*This document should be updated as new features are added or processes change.*



