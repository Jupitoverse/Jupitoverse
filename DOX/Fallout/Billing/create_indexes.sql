-- ============================================================================
-- Index Creation Script for OSO_Service_Activated Query Optimization
-- ============================================================================
-- Author: Abhishek
-- Date: 2025-01-27
-- Purpose: Create indexes to optimize service activation query performance
-- ============================================================================

-- STEP 1: Check existing indexes first
-- Run this to see what already exists:
/*
SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'ossdb01db'
    AND tablename IN (
        'DD_AGREEMENT',
        'DD_SOLUTION_LEG',
        'dd_product_version',
        'SC_PROJECT_ORDER_INSTANCE',
        'oss_activity_instance',
        'oss_attribute_store',
        'DD_SITE_ORDER',
        'dd_project_assignment_details'
    )
ORDER BY tablename, indexname;
*/

-- ============================================================================
-- CRITICAL INDEXES (High Impact - Create These First)
-- ============================================================================

-- Index 1: DD_AGREEMENT - Filtering on is_latest and customer_name
-- Impact: Speeds up main table filtering
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dd_agreement_latest_name 
ON ossdb01db.DD_AGREEMENT(is_latest, customer_name) 
WHERE is_latest = 1;
-- Estimated improvement: 30-40% on agreement filtering

-- Index 2: DD_SOLUTION_LEG - Date and status filtering
-- Impact: Critical for activation_date filter
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dd_solution_leg_status_date 
ON ossdb01db.DD_SOLUTION_LEG(ptd_status, activation_date, solution_name) 
WHERE ptd_status IN ('Activated', 'Completed');
-- Estimated improvement: 40-50% on solution leg filtering

-- Index 3: dd_product_version - Product spec and latest flag
-- Impact: Speeds up product version filtering
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dd_product_version_latest_spec 
ON ossdb01db.dd_product_version(is_latest, product_spec, product_agreement_instance_id) 
WHERE is_latest = 1 AND product_spec IN ('UNI', 'Business_Internet', 'EVC_Endpoint', 'SIP', 'PRI', 'BVE');
-- Estimated improvement: 35-45% on product version filtering

-- Index 4: SC_PROJECT_ORDER_INSTANCE - Version and status filtering
-- Impact: Speeds up project instance joins
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sc_project_latest_status 
ON ossdb01db.SC_PROJECT_ORDER_INSTANCE(is_latest_version, parent_project_id, status) 
WHERE is_latest_version = 1;
-- Estimated improvement: 25-35% on project filtering

-- Index 5: oss_activity_instance - Spec ID and plan filtering
-- Impact: Critical for activity state checks
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_oss_activity_instance_spec_latest 
ON ossdb01db.oss_activity_instance(spec_ver_id, plan_id, is_latest_version, state) 
WHERE is_latest_version = 1;
-- Estimated improvement: 30-40% on activity filtering

-- Index 6: oss_attribute_store - THE MOST CRITICAL INDEX
-- Impact: HUGE - this table is likely very large and already uses part_id
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_oss_attribute_store_partid_code 
ON ossdb01db.oss_attribute_store(part_id, parent_id, code, value) 
WHERE code = 'productId';
-- Estimated improvement: 50-70% on attribute store lookups

-- Index 7: DD_SITE_ORDER - Latest flag with site_id
-- Impact: Speeds up site order filtering
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dd_site_order_latest 
ON ossdb01db.DD_SITE_ORDER(is_latest, site_id) 
WHERE is_latest = 1;
-- Estimated improvement: 20-30% on site order filtering

-- Index 8: dd_project_assignment_details - Assignment filtering
-- Impact: Speeds up CPM assignment lookups
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dd_proj_assign_details 
ON ossdb01db.dd_project_assignment_details(customer_id, framework_agreement_id, site_id, entity_type, type, assignment_status) 
WHERE assignment_status = 'ASSIGNED';
-- Estimated improvement: 25-35% on CPM lookups

-- ============================================================================
-- FOREIGN KEY INDEXES (Important for Joins)
-- ============================================================================

-- Index 9: DD_SOLUTION_LEG foreign key
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dd_solution_leg_agreement 
ON ossdb01db.DD_SOLUTION_LEG(agreement_id);

-- Index 10: DD_SOLUTION_LEG_SITE foreign key
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dd_solution_leg_site_leg 
ON ossdb01db.DD_SOLUTION_LEG_SITE(solution_leg_id);

-- Index 11: DD_SOLUTION_LEG_SITE to site order
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dd_solution_leg_site_order 
ON ossdb01db.DD_SOLUTION_LEG_SITE(site_order_id);

-- Index 12: dd_sol_leg_site_2_prod_version both columns
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_dd_sol_leg_site_2_prod 
ON ossdb01db.dd_sol_leg_site_2_prod_version(solution_leg_site_id, prod_ver_id);

-- ============================================================================
-- POST-INDEX CREATION: Update Statistics
-- ============================================================================

-- After creating indexes, update table statistics for better query planning
ANALYZE ossdb01db.DD_AGREEMENT;
ANALYZE ossdb01db.DD_SOLUTION_LEG;
ANALYZE ossdb01db.dd_product_version;
ANALYZE ossdb01db.SC_PROJECT_ORDER_INSTANCE;
ANALYZE ossdb01db.oss_activity_instance;
ANALYZE ossdb01db.oss_attribute_store;
ANALYZE ossdb01db.DD_SITE_ORDER;
ANALYZE ossdb01db.dd_project_assignment_details;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check if indexes were created successfully
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
FROM pg_indexes
WHERE schemaname = 'ossdb01db'
    AND indexname LIKE 'idx_%'
    AND indexname IN (
        'idx_dd_agreement_latest_name',
        'idx_dd_solution_leg_status_date',
        'idx_dd_product_version_latest_spec',
        'idx_sc_project_latest_status',
        'idx_oss_activity_instance_spec_latest',
        'idx_oss_attribute_store_partid_code',
        'idx_dd_site_order_latest',
        'idx_dd_proj_assign_details'
    )
ORDER BY tablename, indexname;

-- Check index usage statistics (run after query has been executed a few times)
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as times_used,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'ossdb01db'
    AND indexname LIKE 'idx_%'
ORDER BY idx_scan DESC;

-- ============================================================================
-- NOTES
-- ============================================================================

-- 1. CONCURRENTLY keyword allows index creation without locking the table
--    (can be used in production without downtime)
--
-- 2. Creating these indexes may take 10-60 minutes depending on table sizes
--
-- 3. Monitor index creation progress:
--    SELECT * FROM pg_stat_progress_create_index;
--
-- 4. After indexes are created, test your query with EXPLAIN ANALYZE
--
-- 5. If you don't have permission to create indexes, contact your DBA
--
-- 6. Indexes take disk space - estimate 10-30% of table size per index
--
-- 7. part_id index on oss_attribute_store is the most critical - prioritize this!

-- ============================================================================
-- ROLLBACK (if needed)
-- ============================================================================

-- If you need to remove indexes (not recommended unless there's an issue):
/*
DROP INDEX CONCURRENTLY IF EXISTS ossdb01db.idx_dd_agreement_latest_name;
DROP INDEX CONCURRENTLY IF EXISTS ossdb01db.idx_dd_solution_leg_status_date;
DROP INDEX CONCURRENTLY IF EXISTS ossdb01db.idx_dd_product_version_latest_spec;
DROP INDEX CONCURRENTLY IF EXISTS ossdb01db.idx_sc_project_latest_status;
DROP INDEX CONCURRENTLY IF EXISTS ossdb01db.idx_oss_activity_instance_spec_latest;
DROP INDEX CONCURRENTLY IF EXISTS ossdb01db.idx_oss_attribute_store_partid_code;
DROP INDEX CONCURRENTLY IF EXISTS ossdb01db.idx_dd_site_order_latest;
DROP INDEX CONCURRENTLY IF EXISTS ossdb01db.idx_dd_proj_assign_details;
*/

-- ============================================================================
-- END OF SCRIPT
-- ============================================================================


