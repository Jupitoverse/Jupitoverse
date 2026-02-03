-- ============================================================================
-- Enhanced Workaround Inventory Database Schema
-- ============================================================================
-- This schema adds collaborative features: comments, likes, shares, tags
-- ============================================================================

-- 1. Enhanced Workarounds Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS workarounds (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    issue TEXT NOT NULL,
    description TEXT NOT NULL,
    created_by VARCHAR(255) DEFAULT 'Anonymous',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'active',  -- active, archived, draft
    tags TEXT[],  -- Array of tags for easy filtering
    priority VARCHAR(20) DEFAULT 'medium',  -- low, medium, high, critical
    is_verified BOOLEAN DEFAULT FALSE,  -- Verified by admin/expert
    verified_by VARCHAR(255),
    verified_date TIMESTAMP,
    attachments JSONB,  -- Store file references as JSON
    related_srs TEXT[],  -- Array of related SR IDs
    related_defects TEXT[]  -- Array of related Defect IDs
);

-- Index for faster searches
CREATE INDEX IF NOT EXISTS idx_workarounds_category ON workarounds(category);
CREATE INDEX IF NOT EXISTS idx_workarounds_created_by ON workarounds(created_by);
CREATE INDEX IF NOT EXISTS idx_workarounds_tags ON workarounds USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_workarounds_status ON workarounds(status);


-- 2. Comments Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS workaround_comments (
    id SERIAL PRIMARY KEY,
    workaround_id INTEGER NOT NULL REFERENCES workarounds(id) ON DELETE CASCADE,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255),
    comment_text TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_edited BOOLEAN DEFAULT FALSE,
    parent_comment_id INTEGER REFERENCES workaround_comments(id) ON DELETE CASCADE,  -- For nested replies
    likes INTEGER DEFAULT 0,
    is_solution BOOLEAN DEFAULT FALSE  -- Mark if this comment solved the issue
);

-- Index for faster comment retrieval
CREATE INDEX IF NOT EXISTS idx_comments_workaround ON workaround_comments(workaround_id);
CREATE INDEX IF NOT EXISTS idx_comments_parent ON workaround_comments(parent_comment_id);


-- 3. Likes Tracking Table (who liked what)
-- ============================================================================
CREATE TABLE IF NOT EXISTS workaround_likes (
    id SERIAL PRIMARY KEY,
    workaround_id INTEGER NOT NULL REFERENCES workarounds(id) ON DELETE CASCADE,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255),
    liked_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(workaround_id, user_email)  -- Prevent duplicate likes
);

CREATE INDEX IF NOT EXISTS idx_likes_workaround ON workaround_likes(workaround_id);
CREATE INDEX IF NOT EXISTS idx_likes_user ON workaround_likes(user_email);


-- 4. Shares/Bookmarks Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS workaround_shares (
    id SERIAL PRIMARY KEY,
    workaround_id INTEGER NOT NULL REFERENCES workarounds(id) ON DELETE CASCADE,
    shared_by VARCHAR(255) NOT NULL,
    shared_with VARCHAR(255),  -- NULL means public share
    share_type VARCHAR(50) DEFAULT 'bookmark',  -- bookmark, email, link
    share_message TEXT,
    shared_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_shares_workaround ON workaround_shares(workaround_id);
CREATE INDEX IF NOT EXISTS idx_shares_user ON workaround_shares(shared_by);


-- 5. Activity Log Table (audit trail)
-- ============================================================================
CREATE TABLE IF NOT EXISTS workaround_activity_log (
    id SERIAL PRIMARY KEY,
    workaround_id INTEGER REFERENCES workarounds(id) ON DELETE CASCADE,
    user_name VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,  -- created, updated, deleted, commented, liked, shared
    action_details JSONB,  -- Store additional context
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_activity_workaround ON workaround_activity_log(workaround_id);
CREATE INDEX IF NOT EXISTS idx_activity_user ON workaround_activity_log(user_name);
CREATE INDEX IF NOT EXISTS idx_activity_action ON workaround_activity_log(action);


-- 6. Tags/Categories Reference Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS workaround_tags (
    id SERIAL PRIMARY KEY,
    tag_name VARCHAR(100) UNIQUE NOT NULL,
    tag_color VARCHAR(20) DEFAULT '#3b82f6',  -- Hex color for UI
    usage_count INTEGER DEFAULT 0,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tags_name ON workaround_tags(tag_name);


-- 7. User Preferences Table (for personalization)
-- ============================================================================
CREATE TABLE IF NOT EXISTS workaround_user_preferences (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) UNIQUE NOT NULL,
    favorite_categories TEXT[],
    notification_settings JSONB,
    display_preferences JSONB,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Sample Data Insertion (for testing)
-- ============================================================================

-- Insert sample workaround
INSERT INTO workarounds (category, issue, description, created_by, tags, priority, related_srs)
VALUES (
    'OSO',
    'Construction task completed but order not flowing back to Bedrock',
    '<p><strong>Issue:</strong> Construction task was completed in OSO but the order is not flowing back to Bedrock.</p>
    <p><strong>Customer ID:</strong> 130382820<br>
    <strong>Customer Name:</strong> ER2 Image Group<br>
    <strong>Site ID:</strong> OSite_623385_1</p>
    <p><strong>Root Cause:</strong> Manual task "Offnet Order ROE" is getting opened even when ROE_Needed is "No".</p>
    <p><strong>Workaround:</strong></p>
    <ol>
        <li>Check if ROE_Needed flag is "No" in the manual task</li>
        <li>Manually skip the "Offnet Order ROE" task</li>
        <li>Order will flow back to Bedrock after skipping</li>
    </ol>
    <p><strong>Permanent Fix:</strong> Defect #2860119 has been raised to update the design logic.</p>',
    'Vipin Kumar (vkumar121)',
    ARRAY['OSO', 'Bedrock', 'Construction', 'ROE'],
    'high',
    ARRAY['SR019577586', 'SR019523426']
) ON CONFLICT DO NOTHING;

-- Insert sample tags
INSERT INTO workaround_tags (tag_name, tag_color, usage_count) VALUES
    ('OSO', '#3b82f6', 15),
    ('Bedrock', '#8b5cf6', 8),
    ('CLIPS', '#10b981', 12),
    ('Construction', '#f59e0b', 6),
    ('ROE', '#ef4444', 4),
    ('DCP', '#ec4899', 10),
    ('VMS', '#14b8a6', 7)
ON CONFLICT (tag_name) DO NOTHING;

-- ============================================================================
-- Useful Queries
-- ============================================================================

-- Get workarounds with comment count
-- SELECT w.*, COUNT(c.id) as comment_count 
-- FROM workarounds w 
-- LEFT JOIN workaround_comments c ON w.id = c.workaround_id 
-- GROUP BY w.id 
-- ORDER BY w.created_date DESC;

-- Get most popular workarounds (by views + likes)
-- SELECT *, (views + (likes * 2)) as popularity_score 
-- FROM workarounds 
-- ORDER BY popularity_score DESC 
-- LIMIT 10;

-- Get trending workarounds (last 7 days)
-- SELECT w.*, COUNT(al.id) as activity_count 
-- FROM workarounds w 
-- INNER JOIN workaround_activity_log al ON w.id = al.workaround_id 
-- WHERE al.created_date >= NOW() - INTERVAL '7 days' 
-- GROUP BY w.id 
-- ORDER BY activity_count DESC 
-- LIMIT 10;

