# backend/routes/workarounds_enhanced.py
"""
Enhanced Workaround Management API
Includes: Comments, Likes, Shares, Tags, Activity Tracking
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import psycopg2
import psycopg2.extras
import database

workarounds_bp = Blueprint('workarounds', __name__)

# ============================================================================
# WORKAROUND CRUD OPERATIONS
# ============================================================================

@workarounds_bp.route('/', methods=['GET'])
def get_workarounds():
    """
    Get all workarounds with additional metrics (comments count, likes, etc.)
    Query params: status, category, tag, limit, offset, sort_by
    """
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get query parameters
        status = request.args.get('status', 'active')
        category = request.args.get('category')
        tag = request.args.get('tag')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        sort_by = request.args.get('sort_by', 'created_date')  # created_date, views, likes, popularity
        
        # Build query dynamically
        query = """
            SELECT 
                w.*,
                COUNT(DISTINCT c.id) as comment_count,
                (w.views + (w.likes * 2) + (w.shares * 3)) as popularity_score
            FROM workarounds w
            LEFT JOIN workaround_comments c ON w.id = c.workaround_id
            WHERE w.status = %s
        """
        params = [status]
        
        if category:
            query += " AND w.category = %s"
            params.append(category)
        
        if tag:
            query += " AND %s = ANY(w.tags)"
            params.append(tag)
        
        query += " GROUP BY w.id"
        
        # Add sorting
        if sort_by == 'popularity':
            query += " ORDER BY popularity_score DESC"
        elif sort_by == 'views':
            query += " ORDER BY w.views DESC"
        elif sort_by == 'likes':
            query += " ORDER BY w.likes DESC"
        else:
            query += " ORDER BY w.created_date DESC"
        
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cur.execute(query, params)
        workarounds = cur.fetchall()
        
        # Get total count
        count_query = "SELECT COUNT(*) FROM workarounds WHERE status = %s"
        count_params = [status]
        if category:
            count_query += " AND category = %s"
            count_params.append(category)
        if tag:
            count_query += " AND %s = ANY(tags)"
            count_params.append(tag)
        
        cur.execute(count_query, count_params)
        total_count = cur.fetchone()['count']
        
        cur.close()
        conn.close()
        
        return jsonify({
            'workarounds': [dict(w) for w in workarounds],
            'total': total_count,
            'limit': limit,
            'offset': offset
        })
    
    except Exception as e:
        print(f"❌ Error fetching workarounds: {e}")
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


@workarounds_bp.route('/', methods=['POST'])
def add_workaround():
    """Create a new workaround"""
    data = request.get_json()
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Insert workaround
        cur.execute(
            """INSERT INTO workarounds 
               (category, issue, description, created_by, tags, priority, 
                related_srs, related_defects, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING *""",
            (
                data.get('category'),
                data.get('issue'),
                data.get('description'),
                data.get('created_by', 'Anonymous'),
                data.get('tags', []),
                data.get('priority', 'medium'),
                data.get('related_srs', []),
                data.get('related_defects', []),
                data.get('status', 'active')
            )
        )
        new_workaround = dict(cur.fetchone())
        
        # Log activity
        log_activity(conn, new_workaround['id'], data.get('created_by', 'Anonymous'), 
                    'created', {'workaround': new_workaround})
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'status': 'success', 'workaround': new_workaround}), 201
    
    except Exception as e:
        print(f"❌ Error creating workaround: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


@workarounds_bp.route('/<int:id>', methods=['GET'])
def get_workaround(id):
    """Get a single workaround with all details including comments"""
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get workaround
        cur.execute("SELECT * FROM workarounds WHERE id = %s", (id,))
        workaround = cur.fetchone()
        
        if not workaround:
            return jsonify({'error': 'Workaround not found'}), 404
        
        # Get comments
        cur.execute("""
            SELECT * FROM workaround_comments 
            WHERE workaround_id = %s 
            ORDER BY created_date ASC
        """, (id,))
        comments = cur.fetchall()
        
        # Increment view count
        cur.execute("UPDATE workarounds SET views = views + 1 WHERE id = %s", (id,))
        conn.commit()
        
        result = dict(workaround)
        result['comments'] = [dict(c) for c in comments]
        result['views'] = result['views'] + 1  # Show updated view count
        
        cur.close()
        conn.close()
        
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Error fetching workaround: {e}")
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


@workarounds_bp.route('/<int:id>', methods=['PUT'])
def update_workaround(id):
    """Update a workaround"""
    data = request.get_json()
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute(
            """UPDATE workarounds 
               SET category = %s, issue = %s, description = %s, 
                   tags = %s, priority = %s, updated_date = CURRENT_TIMESTAMP,
                   related_srs = %s, related_defects = %s
               WHERE id = %s
               RETURNING *""",
            (
                data.get('category'),
                data.get('issue'),
                data.get('description'),
                data.get('tags', []),
                data.get('priority', 'medium'),
                data.get('related_srs', []),
                data.get('related_defects', []),
                id
            )
        )
        
        updated_workaround = cur.fetchone()
        if not updated_workaround:
            return jsonify({'error': 'Workaround not found'}), 404
        
        # Log activity
        log_activity(conn, id, data.get('updated_by', 'Anonymous'), 
                    'updated', {'changes': data})
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'status': 'success', 'workaround': dict(updated_workaround)})
    
    except Exception as e:
        print(f"❌ Error updating workaround: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


@workarounds_bp.route('/<int:id>', methods=['DELETE'])
def delete_workaround(id):
    """Delete or archive a workaround"""
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        
        # Soft delete (archive) instead of hard delete
        cur.execute(
            "UPDATE workarounds SET status = 'archived' WHERE id = %s",
            (id,)
        )
        
        if cur.rowcount == 0:
            return jsonify({'error': 'Workaround not found'}), 404
        
        # Log activity
        log_activity(conn, id, 'System', 'archived', None)
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Workaround archived'})
    
    except Exception as e:
        print(f"❌ Error deleting workaround: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# COMMENTS OPERATIONS
# ============================================================================

@workarounds_bp.route('/<int:id>/comments', methods=['GET'])
def get_comments(id):
    """Get all comments for a workaround"""
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT * FROM workaround_comments 
            WHERE workaround_id = %s 
            ORDER BY created_date ASC
        """, (id,))
        comments = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify([dict(c) for c in comments])
    
    except Exception as e:
        print(f"❌ Error fetching comments: {e}")
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


@workarounds_bp.route('/<int:id>/comments', methods=['POST'])
def add_comment(id):
    """Add a comment to a workaround"""
    data = request.get_json()
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute(
            """INSERT INTO workaround_comments 
               (workaround_id, user_name, user_email, comment_text, parent_comment_id, is_solution)
               VALUES (%s, %s, %s, %s, %s, %s)
               RETURNING *""",
            (
                id,
                data.get('user_name', 'Anonymous'),
                data.get('user_email'),
                data.get('comment_text'),
                data.get('parent_comment_id'),
                data.get('is_solution', False)
            )
        )
        new_comment = dict(cur.fetchone())
        
        # Log activity
        log_activity(conn, id, data.get('user_name', 'Anonymous'), 
                    'commented', {'comment': new_comment})
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'status': 'success', 'comment': new_comment}), 201
    
    except Exception as e:
        print(f"❌ Error adding comment: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


@workarounds_bp.route('/<int:id>/comments/<int:comment_id>', methods=['PUT'])
def update_comment(id, comment_id):
    """Update a comment"""
    data = request.get_json()
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute(
            """UPDATE workaround_comments 
               SET comment_text = %s, is_edited = TRUE, updated_date = CURRENT_TIMESTAMP
               WHERE id = %s AND workaround_id = %s
               RETURNING *""",
            (data.get('comment_text'), comment_id, id)
        )
        
        updated_comment = cur.fetchone()
        if not updated_comment:
            return jsonify({'error': 'Comment not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'status': 'success', 'comment': dict(updated_comment)})
    
    except Exception as e:
        print(f"❌ Error updating comment: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


@workarounds_bp.route('/<int:id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(id, comment_id):
    """Delete a comment"""
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM workaround_comments WHERE id = %s AND workaround_id = %s",
            (comment_id, id)
        )
        
        if cur.rowcount == 0:
            return jsonify({'error': 'Comment not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Comment deleted'})
    
    except Exception as e:
        print(f"❌ Error deleting comment: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# LIKES OPERATIONS
# ============================================================================

@workarounds_bp.route('/<int:id>/like', methods='POST'])
def toggle_like(id):
    """Toggle like on a workaround (like/unlike)"""
    data = request.get_json()
    user_email = data.get('user_email', 'anonymous@example.com')
    user_name = data.get('user_name', 'Anonymous')
    
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Check if already liked
        cur.execute(
            "SELECT id FROM workaround_likes WHERE workaround_id = %s AND user_email = %s",
            (id, user_email)
        )
        existing_like = cur.fetchone()
        
        if existing_like:
            # Unlike
            cur.execute(
                "DELETE FROM workaround_likes WHERE workaround_id = %s AND user_email = %s",
                (id, user_email)
            )
            cur.execute(
                "UPDATE workarounds SET likes = GREATEST(likes - 1, 0) WHERE id = %s",
                (id,)
            )
            action = 'unliked'
        else:
            # Like
            cur.execute(
                """INSERT INTO workaround_likes (workaround_id, user_name, user_email)
                   VALUES (%s, %s, %s)""",
                (id, user_name, user_email)
            )
            cur.execute(
                "UPDATE workarounds SET likes = likes + 1 WHERE id = %s",
                (id,)
            )
            action = 'liked'
            log_activity(conn, id, user_name, 'liked', None)
        
        # Get updated like count
        cur.execute("SELECT likes FROM workarounds WHERE id = %s", (id,))
        likes = cur.fetchone()['likes']
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'status': 'success', 'action': action, 'likes': likes})
    
    except Exception as e:
        print(f"❌ Error toggling like: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# SHARE OPERATIONS
# ============================================================================

@workarounds_bp.route('/<int:id>/share', methods=['POST'])
def share_workaround(id):
    """Share or bookmark a workaround"""
    data = request.get_json()
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute(
            """INSERT INTO workaround_shares 
               (workaround_id, shared_by, shared_with, share_type, share_message)
               VALUES (%s, %s, %s, %s, %s)
               RETURNING *""",
            (
                id,
                data.get('shared_by', 'Anonymous'),
                data.get('shared_with'),
                data.get('share_type', 'bookmark'),
                data.get('share_message')
            )
        )
        share = dict(cur.fetchone())
        
        # Update share count
        cur.execute("UPDATE workarounds SET shares = shares + 1 WHERE id = %s", (id,))
        
        # Log activity
        log_activity(conn, id, data.get('shared_by', 'Anonymous'), 
                    'shared', {'share_type': data.get('share_type')})
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'status': 'success', 'share': share}), 201
    
    except Exception as e:
        print(f"❌ Error sharing workaround: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# STATISTICS & ANALYTICS
# ============================================================================

@workarounds_bp.route('/stats', methods=['GET'])
def get_statistics():
    """Get overall workaround statistics"""
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Total counts
        cur.execute("""
            SELECT 
                COUNT(*) as total_workarounds,
                SUM(views) as total_views,
                SUM(likes) as total_likes,
                SUM(shares) as total_shares,
                COUNT(DISTINCT category) as total_categories
            FROM workarounds
            WHERE status = 'active'
        """)
        stats = dict(cur.fetchone())
        
        # Get comment count
        cur.execute("SELECT COUNT(*) as total_comments FROM workaround_comments")
        stats.update(cur.fetchone())
        
        # Most popular workarounds
        cur.execute("""
            SELECT id, issue, views, likes, shares,
                   (views + (likes * 2) + (shares * 3)) as popularity_score
            FROM workarounds
            WHERE status = 'active'
            ORDER BY popularity_score DESC
            LIMIT 5
        """)
        stats['most_popular'] = [dict(r) for r in cur.fetchall()]
        
        # Most active categories
        cur.execute("""
            SELECT category, COUNT(*) as count
            FROM workarounds
            WHERE status = 'active'
            GROUP BY category
            ORDER BY count DESC
            LIMIT 5
        """)
        stats['top_categories'] = [dict(r) for r in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return jsonify(stats)
    
    except Exception as e:
        print(f"❌ Error fetching statistics: {e}")
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# TAGS OPERATIONS
# ============================================================================

@workarounds_bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all available tags"""
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM workaround_tags ORDER BY usage_count DESC")
        tags = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify([dict(t) for t in tags])
    
    except Exception as e:
        print(f"❌ Error fetching tags: {e}")
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def log_activity(conn, workaround_id, user_name, action, details):
    """Log activity to audit trail"""
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO workaround_activity_log 
               (workaround_id, user_name, action, action_details)
               VALUES (%s, %s, %s, %s)""",
            (workaround_id, user_name, action, psycopg2.extras.Json(details) if details else None)
        )
        cur.close()
    except Exception as e:
        print(f"Warning: Failed to log activity: {e}")






