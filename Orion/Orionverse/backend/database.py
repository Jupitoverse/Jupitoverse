# backend/database.py
"""
Data Access Layer for Orionverse Hub

This module handles all database connections and operations.
SECURITY WARNING: Credentials are currently hardcoded. 
TODO: Move to environment variables before production deployment.
"""

import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash


def get_db_connection():
    """
    Establishes and returns a PostgreSQL database connection.
    
    Returns:
        psycopg2.connection: Database connection object, or None if connection fails
    
    ⚠️ WARNING: This function contains hardcoded credentials and is NOT secure.
    It is highly recommended to use environment variables and a .env file instead.
    
    Example secure implementation:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        conn = psycopg2.connect(
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
    """
    try:
        conn = psycopg2.connect(
            database="prodossdb",
            user='ossdb01uams',
            password='Pr0d_ossdb01uams',
            host='oso-pstgr-rd.orion.comcast.com',
            port='6432'
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ DATABASE CONNECTION FAILED: {e}")
        return None


# ============================================================================
# USER MANAGEMENT FUNCTIONS
# ============================================================================

def create_user(fullname, email, password):
    """
    Creates a new user account with hashed password.
    
    Args:
        fullname (str): User's full name
        email (str): User's email address (must be unique)
        password (str): Plain text password (will be hashed)
    
    Returns:
        dict: User object with id, fullname, email, role, status
        None: If email already exists or connection fails
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Check if email already exists
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return None
        
        # Hash password and insert new user
        password_hash = generate_password_hash(password)
        cur.execute(
            """INSERT INTO users (fullname, email, password_hash, role, status)
               VALUES (%s, %s, %s, 'user', 'pending')
               RETURNING id, fullname, email, role, status""",
            (fullname, email, password_hash)
        )
        new_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return dict(new_user)
    
    except psycopg2.Error as e:
        print(f"❌ ERROR creating user: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return None


def find_user_by_email(email):
    """
    Retrieves a user by their email address.
    
    Args:
        email (str): User's email address
    
    Returns:
        dict: User object including password_hash (for verification)
        None: If user not found or connection fails
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return dict(user) if user else None
    
    except psycopg2.Error as e:
        print(f"❌ ERROR finding user: {e}")
        if conn:
            conn.close()
        return None


def get_all_users():
    """
    Retrieves all users from the database (for admin use).
    
    Returns:
        list: List of user dictionaries (without password_hash)
        []: Empty list if connection fails or no users exist
    """
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            """SELECT id, fullname, email, role, status, created_at 
               FROM users 
               ORDER BY created_at DESC"""
        )
        users = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(user) for user in users]
    
    except psycopg2.Error as e:
        print(f"❌ ERROR fetching users: {e}")
        if conn:
            conn.close()
        return []


def update_user_status(user_id, status):
    """
    Updates a user's account status (for admin approval/rejection).
    
    Args:
        user_id (int): User's database ID
        status (str): New status ('approved', 'rejected', 'pending')
    
    Returns:
        bool: True if update successful, False otherwise
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET status = %s WHERE id = %s",
            (status, user_id)
        )
        conn.commit()
        success = cur.rowcount > 0
        cur.close()
        conn.close()
        return success
    
    except psycopg2.Error as e:
        print(f"❌ ERROR updating user status: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return False


# ============================================================================
# WORKAROUND MANAGEMENT FUNCTIONS
# ============================================================================

def update_workaround(id, data):
    """
    Updates an existing workaround in the database.
    
    Args:
        id (int): Workaround ID
        data (dict): Dictionary with 'category', 'issue', 'description'
    
    Returns:
        bool: True if update successful, False otherwise
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute(
            """UPDATE workarounds 
               SET category = %s, issue = %s, description = %s
               WHERE id = %s""",
            (data['category'], data['issue'], data['description'], id)
        )
        conn.commit()
        success = cur.rowcount > 0
        cur.close()
        conn.close()
        return success
    
    except psycopg2.Error as e:
        print(f"❌ ERROR updating workaround: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return False


def delete_workaround(id):
    """
    Deletes a workaround from the database.
    
    Args:
        id (int): Workaround ID
    
    Returns:
        bool: True if deletion successful, False otherwise
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
    cur = conn.cursor()
    cur.execute("DELETE FROM workarounds WHERE id = %s", (id,))
    conn.commit()
        success = cur.rowcount > 0
        cur.close()
        conn.close()
        return success
    
    except psycopg2.Error as e:
        print(f"❌ ERROR deleting workaround: {e}")
        conn.rollback()
        if conn:
            conn.close()
        return False


def get_workaround_by_id(id):
    """
    Retrieves a single workaround by ID.
    
    Args:
        id (int): Workaround ID
    
    Returns:
        dict: Workaround object
        None: If not found or connection fails
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM workarounds WHERE id = %s", (id,))
        workaround = cur.fetchone()
        cur.close()
        conn.close()
        return dict(workaround) if workaround else None
    
    except psycopg2.Error as e:
        print(f"❌ ERROR fetching workaround: {e}")
        if conn:
            conn.close()
        return None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def test_connection():
    """
    Tests the database connection.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1")
    cur.close()
    conn.close()
            print("✅ Database connection successful!")
            return True
        except psycopg2.Error as e:
            print(f"❌ Database query failed: {e}")
            if conn:
                conn.close()
            return False
    return False


if __name__ == '__main__':
    # Test connection when running this file directly
    test_connection()