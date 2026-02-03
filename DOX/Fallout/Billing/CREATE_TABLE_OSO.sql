-- ============================================================================
-- OSO Service Activated Data - Table Creation Script
-- ============================================================================
-- Database: prodossdb
-- Purpose: Track service activations not yet billing
-- Created: 2025-11-29
-- ============================================================================

-- Drop table if exists (use with caution!)
-- DROP TABLE IF EXISTS OSO_Service_Activated_Data CASCADE;

-- Create table with full schema
CREATE TABLE IF NOT EXISTS OSO_Service_Activated_Data (
    -- Primary data columns from query (26 columns)
    customer_id TEXT,
    site_id TEXT,
    service_id TEXT NOT NULL,
    product_agreement_instance_id TEXT,
    solution_id TEXT,
    version TEXT NOT NULL,
    ptd TEXT,
    customer_name TEXT,
    framework_agreement_id TEXT,
    division TEXT,
    region TEXT,
    business_action TEXT,
    solution_leg_state TEXT,
    solution_name TEXT,
    ptd_status TEXT,
    activation_date TEXT,
    customer_accepted TEXT,
    product_spec TEXT,
    send_to_billing TEXT,
    cpm TEXT,
    customer_acceptance_days TEXT,
    customer_acceptance_state TEXT,
    customer_acceptance_plan_id TEXT,
    customer_acceptance_activity_id TEXT,
    ticketid TEXT,
    create_ticket TEXT,
    
    -- Tracking columns for RCA and status management (8 columns)
    RCA TEXT,
    RCA_Category TEXT,
    Owned_By TEXT,
    WorkQueue TEXT,
    Task_Owner TEXT,
    Tracking_ID TEXT,
    Next_Action TEXT,
    Handling_Status TEXT,
    
    -- Metadata columns for audit trail (2 columns)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Composite unique constraint to prevent duplicates
    CONSTRAINT unique_service_site_version UNIQUE (service_id, site_id, version)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_oso_service_activated_customer_id 
    ON OSO_Service_Activated_Data(customer_id);

CREATE INDEX IF NOT EXISTS idx_oso_service_activated_site_id 
    ON OSO_Service_Activated_Data(site_id);

CREATE INDEX IF NOT EXISTS idx_oso_service_activated_service_id 
    ON OSO_Service_Activated_Data(service_id);

CREATE INDEX IF NOT EXISTS idx_oso_service_activated_ptd_status 
    ON OSO_Service_Activated_Data(ptd_status);

CREATE INDEX IF NOT EXISTS idx_oso_service_activated_activation_date 
    ON OSO_Service_Activated_Data(activation_date);

CREATE INDEX IF NOT EXISTS idx_oso_service_activated_created_at 
    ON OSO_Service_Activated_Data(created_at);

-- Add comments to table and key columns
COMMENT ON TABLE OSO_Service_Activated_Data IS 
'Tracks service activations that are not yet billing. Populated by OSO_Service_Activated.py script.';

COMMENT ON COLUMN OSO_Service_Activated_Data.service_id IS 
'Unique service identifier (part of composite unique key)';

COMMENT ON COLUMN OSO_Service_Activated_Data.site_id IS 
'Site identifier (part of composite unique key)';

COMMENT ON COLUMN OSO_Service_Activated_Data.version IS 
'Service version (part of composite unique key)';

COMMENT ON COLUMN OSO_Service_Activated_Data.RCA IS 
'Root Cause Analysis - manually populated';

COMMENT ON COLUMN OSO_Service_Activated_Data.Handling_Status IS 
'Current handling status - manually updated';

-- Verify table creation
SELECT 'Table created successfully!' AS status;

-- Show table structure
\d OSO_Service_Activated_Data

-- Show record count (should be 0 initially)
SELECT COUNT(*) AS initial_record_count FROM OSO_Service_Activated_Data;

-- ============================================================================
-- Grant permissions (adjust as needed for your environment)
-- ============================================================================
-- GRANT SELECT, INSERT, UPDATE ON OSO_Service_Activated_Data TO ossdb01db;
-- GRANT USAGE, SELECT ON SEQUENCE oso_service_activated_data_id_seq TO ossdb01db;

-- ============================================================================
-- End of script
-- ============================================================================












