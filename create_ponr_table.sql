-- PostgreSQL table creation script for PONR data storage
-- Run this manually in your PostgreSQL database

CREATE TABLE IF NOT EXISTS ossdb01db.billing_flag_tracking (
    unique_id VARCHAR(100) PRIMARY KEY,
    projectid BIGINT NOT NULL,
    version INTEGER,
    activity_status VARCHAR(50),
    project_status VARCHAR(50),
    activity_id BIGINT,
    name VARCHAR(500),
    last_update_date TIMESTAMP,
    create_date TIMESTAMP,
    identified_date DATE NOT NULL DEFAULT CURRENT_DATE,
    tag VARCHAR(50) NOT NULL DEFAULT 'RELEASE_PONR',
    rca TEXT,
    handling_status VARCHAR(100) DEFAULT 'PENDING',
    age_days INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_billing_flag_tracking_projectid ON ossdb01db.billing_flag_tracking(projectid);
CREATE INDEX IF NOT EXISTS idx_billing_flag_tracking_identified_date ON ossdb01db.billing_flag_tracking(identified_date);
CREATE INDEX IF NOT EXISTS idx_billing_flag_tracking_tag ON ossdb01db.billing_flag_tracking(tag);
CREATE INDEX IF NOT EXISTS idx_billing_flag_tracking_handling_status ON ossdb01db.billing_flag_tracking(handling_status);
CREATE INDEX IF NOT EXISTS idx_billing_flag_tracking_unique_id ON ossdb01db.billing_flag_tracking(unique_id);

-- Add comments for documentation
COMMENT ON TABLE ossdb01db.billing_flag_tracking IS 'Table to track billing flag issues (PONR, etc.) and their resolution status';
COMMENT ON COLUMN ossdb01db.billing_flag_tracking.unique_id IS 'Unique identifier format: RP_projectid_age_days (e.g., RP_12345_15)';
COMMENT ON COLUMN ossdb01db.billing_flag_tracking.identified_date IS 'Date when the issue was first identified by the script';
COMMENT ON COLUMN ossdb01db.billing_flag_tracking.tag IS 'Tag to identify the source script (RELEASE_PONR, etc.)';
COMMENT ON COLUMN ossdb01db.billing_flag_tracking.rca IS 'Root Cause Analysis - to be filled manually';
COMMENT ON COLUMN ossdb01db.billing_flag_tracking.handling_status IS 'Current status: PENDING, IN_PROGRESS, RESOLVED, CLOSED';
COMMENT ON COLUMN ossdb01db.billing_flag_tracking.age_days IS 'Age in days calculated as CURRENT_DATE - last_update_date';

-- Grant necessary permissions (adjust as per your database setup)
-- GRANT SELECT, INSERT, UPDATE ON ossdb01db.billing_flag_tracking TO your_application_user;
