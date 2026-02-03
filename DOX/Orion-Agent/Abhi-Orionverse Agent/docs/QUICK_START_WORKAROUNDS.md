# 🚀 Quick Start - Enhanced Workarounds

## ⚡ 5-Minute Setup

### 1. Run Database Schema
```bash
psql -h oso-pstgr-rd.orion.comcast.com -p 6432 -U ossdb01uams -d prodossdb \
     -f backend/schema_workarounds_enhanced.sql
```

### 2. Update Backend
```bash
cd backend/routes
mv workarounds.py workarounds_old.py
mv workarounds_enhanced.py workarounds.py
# Backend will auto-reload
```

### 3. Test It!
```bash
# Get statistics
curl http://127.0.0.1:5001/api/workarounds/stats

# Create workaround
curl -X POST http://127.0.0.1:5001/api/workarounds/ \
  -H "Content-Type: application/json" \
  -d '{
    "category": "OSO",
    "issue": "Test Issue",
    "description": "<p>Test solution</p>",
    "created_by": "Test User",
    "tags": ["OSO", "Test"],
    "priority": "medium"
  }'
```

---

## 📡 Essential API Calls

### Get All Workarounds
```javascript
GET /api/workarounds/?category=OSO&sort_by=popularity&limit=10
```

### Create Workaround
```javascript
POST /api/workarounds/
Body: {
  "category": "OSO",
  "issue": "Problem description",
  "description": "<p>Solution</p>",
  "created_by": "Your Name",
  "tags": ["OSO", "Tag1"],
  "priority": "high",
  "related_srs": ["SR123"]
}
```

### Add Comment
```javascript
POST /api/workarounds/1/comments
Body: {
  "user_name": "John Doe",
  "user_email": "jdoe@comcast.com",
  "comment_text": "Great solution!",
  "is_solution": true
}
```

### Like Workaround
```javascript
POST /api/workarounds/1/like
Body: {
  "user_name": "John Doe",
  "user_email": "jdoe@comcast.com"
}
```

### Bookmark/Share
```javascript
POST /api/workarounds/1/share
Body: {
  "shared_by": "John Doe",
  "share_type": "bookmark"
}
```

---

## 🎯 Query Parameters

```
?status=active|archived|draft
?category=OSO|CLIPS|Bedrock
?tag=Construction|ROE
?sort_by=created_date|views|likes|popularity
?limit=50
?offset=0
```

**Example:**
```
GET /api/workarounds/?category=OSO&tag=Bedrock&sort_by=popularity&limit=20
```

---

## 📊 Get Statistics
```javascript
GET /api/workarounds/stats

Response: {
  "total_workarounds": 150,
  "total_views": 5420,
  "total_likes": 320,
  "total_comments": 87,
  "most_popular": [...],
  "top_categories": [...]
}
```

---

## 🏷️ Get Tags
```javascript
GET /api/workarounds/tags

Response: [
  {"tag_name": "OSO", "tag_color": "#3b82f6", "usage_count": 15},
  {"tag_name": "Bedrock", "tag_color": "#8b5cf6", "usage_count": 8},
  ...
]
```

---

## ✅ Success Response
```json
{
  "status": "success",
  "workaround": { "id": 1, ... },
  "message": "Created successfully"
}
```

## ❌ Error Response
```json
{
  "error": "Error message here",
  "status": 500
}
```

---

## 📚 Full Documentation
- **`WORKAROUND_SETUP_GUIDE.md`** - Complete setup & API docs
- **`WORKAROUND_FEATURES_SUMMARY.md`** - Features overview
- **`schema_workarounds_enhanced.sql`** - Database schema

---

## 🎉 Ready to Use!

**All backend is complete!** Frontend integration next.





