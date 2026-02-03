# -*- coding: utf-8 -*-
"""
Quick test script to debug WRITE DB connection issues.
Tests various connection parameters and provides detailed diagnostics.
"""

import psycopg2
import sys
from datetime import datetime

print("=" * 80)
print("WRITE DB Connection Diagnostic Tool")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# Configuration
WRITE_DB_CONFIG = {
    'host': 'OSS-PROD1-PGRDS-NLB-1fe6faf4eb2c6ea3.elb.us-east-2.amazonaws.com',
    'database': 'prodossdb',
    'port': 6432,
    'user': 'ossdb01db',
    'password': 'Pr0d_ossdb01db',
}

print("\nConfiguration:")
print(f"  Host: {WRITE_DB_CONFIG['host']}")
print(f"  Port: {WRITE_DB_CONFIG['port']}")
print(f"  Database: {WRITE_DB_CONFIG['database']}")
print(f"  User: {WRITE_DB_CONFIG['user']}")
print("=" * 80)

# Test 1: Basic Connection (30 second timeout)
print("\nTest 1: Basic Connection (30s timeout)...")
try:
    conn = psycopg2.connect(
        host=WRITE_DB_CONFIG['host'],
        port=WRITE_DB_CONFIG['port'],
        user=WRITE_DB_CONFIG['user'],
        password=WRITE_DB_CONFIG['password'],
        database=WRITE_DB_CONFIG['database'],
        connect_timeout=30
    )
    print("  ✓ Connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"  Database Version: {version[:60]}...")
    
    cursor.close()
    conn.close()
    print("  ✓ Test 1: PASSED")
except Exception as e:
    print(f"  ✗ Test 1: FAILED - {e}")

# Test 2: Extended Timeout (60 seconds)
print("\nTest 2: Extended Timeout (60s)...")
try:
    conn = psycopg2.connect(
        host=WRITE_DB_CONFIG['host'],
        port=WRITE_DB_CONFIG['port'],
        user=WRITE_DB_CONFIG['user'],
        password=WRITE_DB_CONFIG['password'],
        database=WRITE_DB_CONFIG['database'],
        connect_timeout=60
    )
    print("  ✓ Connection successful with 60s timeout!")
    conn.close()
    print("  ✓ Test 2: PASSED")
except Exception as e:
    print(f"  ✗ Test 2: FAILED - {e}")

# Test 3: With SSL Disable
print("\nTest 3: Connection with SSL Disabled...")
try:
    conn = psycopg2.connect(
        host=WRITE_DB_CONFIG['host'],
        port=WRITE_DB_CONFIG['port'],
        user=WRITE_DB_CONFIG['user'],
        password=WRITE_DB_CONFIG['password'],
        database=WRITE_DB_CONFIG['database'],
        connect_timeout=30,
        sslmode='disable'
    )
    print("  ✓ Connection successful with SSL disabled!")
    conn.close()
    print("  ✓ Test 3: PASSED")
except Exception as e:
    print(f"  ✗ Test 3: FAILED - {e}")

# Test 4: With SSL Prefer
print("\nTest 4: Connection with SSL Prefer...")
try:
    conn = psycopg2.connect(
        host=WRITE_DB_CONFIG['host'],
        port=WRITE_DB_CONFIG['port'],
        user=WRITE_DB_CONFIG['user'],
        password=WRITE_DB_CONFIG['password'],
        database=WRITE_DB_CONFIG['database'],
        connect_timeout=30,
        sslmode='prefer'
    )
    print("  ✓ Connection successful with SSL prefer!")
    conn.close()
    print("  ✓ Test 4: PASSED")
except Exception as e:
    print(f"  ✗ Test 4: FAILED - {e}")

# Test 5: Check Table Permissions
print("\nTest 5: Check Table Permissions...")
try:
    conn = psycopg2.connect(
        host=WRITE_DB_CONFIG['host'],
        port=WRITE_DB_CONFIG['port'],
        user=WRITE_DB_CONFIG['user'],
        password=WRITE_DB_CONFIG['password'],
        database=WRITE_DB_CONFIG['database'],
        connect_timeout=30
    )
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'OSO_Service_Activated_Data'
        );
    """)
    table_exists = cursor.fetchone()[0]
    
    if table_exists:
        print("  ✓ Table 'OSO_Service_Activated_Data' exists")
        
        # Try to count records
        cursor.execute("SELECT COUNT(*) FROM OSO_Service_Activated_Data;")
        count = cursor.fetchone()[0]
        print(f"  ✓ Table has {count} records")
        
        # Try to insert a test record (then rollback)
        try:
            cursor.execute("""
                INSERT INTO OSO_Service_Activated_Data (
                    customer_id, site_id, service_id, version
                ) VALUES (
                    'TEST_CUSTOMER', 'TEST_SITE', 'TEST_SERVICE', 'TEST_VERSION'
                )
            """)
            conn.rollback()  # Don't commit, just testing
            print("  ✓ INSERT permission verified")
        except Exception as e:
            print(f"  ✗ INSERT permission test failed: {e}")
    else:
        print("  ℹ Table 'OSO_Service_Activated_Data' does not exist yet")
        print("  ℹ This is normal if running for the first time")
    
    cursor.close()
    conn.close()
    print("  ✓ Test 5: PASSED")
except Exception as e:
    print(f"  ✗ Test 5: FAILED - {e}")

# Test 6: Network Latency
print("\nTest 6: Measuring Connection Latency...")
import time
try:
    start_time = time.time()
    conn = psycopg2.connect(
        host=WRITE_DB_CONFIG['host'],
        port=WRITE_DB_CONFIG['port'],
        user=WRITE_DB_CONFIG['user'],
        password=WRITE_DB_CONFIG['password'],
        database=WRITE_DB_CONFIG['database'],
        connect_timeout=30
    )
    end_time = time.time()
    latency = (end_time - start_time) * 1000  # Convert to milliseconds
    
    print(f"  ✓ Connection established in {latency:.2f} ms")
    
    if latency < 100:
        print("  ✓ Excellent latency (< 100ms)")
    elif latency < 500:
        print("  ℹ Good latency (100-500ms)")
    elif latency < 1000:
        print("  ⚠ Moderate latency (500-1000ms)")
    else:
        print("  ⚠ High latency (> 1000ms) - may need timeout adjustment")
    
    conn.close()
    print("  ✓ Test 6: PASSED")
except Exception as e:
    print(f"  ✗ Test 6: FAILED - {e}")

print("\n" + "=" * 80)
print("Diagnostic Complete")
print("=" * 80)

print("\nRecommendations:")
print("  1. If all tests passed: WRITE DB connection is working correctly")
print("  2. If Test 1 failed but Test 2 passed: Increase connect_timeout to 60")
print("  3. If Test 3 or 4 passed: Adjust sslmode setting")
print("  4. If Test 5 failed: Check database permissions for user 'ossdb01db'")
print("  5. If all tests failed: Check network/firewall/VPN connectivity")
print("=" * 80)












