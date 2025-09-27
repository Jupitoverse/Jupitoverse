# backend/database.py

import psycopg2
# ... other imports ...

def get_db_connection():
    """
    !!! WARNING: This function contains hardcoded credentials and is NOT secure.
    It is highly recommended to use environment variables and a .env file instead.
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

# ... the rest of your functions (create_user, find_user_by_email) ...



# Add these two functions to backend/database.py

def update_workaround(id, data):
    """Updates an existing workaround in the database."""
    conn = get_db_connection()
    if not conn: return None
    
    cur = conn.cursor()
    cur.execute(
        """UPDATE workarounds 
           SET category = %s, issue = %s, description = %s
           WHERE id = %s""",
        (data['category'], data['issue'], data['description'], id)
    )
    conn.commit()
    updated_rows = cur.rowcount
    cur.close()
    conn.close()
    return updated_rows > 0

def delete_workaround(id):
    """Deletes a workaround from the database."""
    conn = get_db_connection()
    if not conn: return None
    
    cur = conn.cursor()
    cur.execute("DELETE FROM workarounds WHERE id = %s", (id,))
    conn.commit()
    deleted_rows = cur.rowcount
    cur.close()
    conn.close()
    return deleted_rows > 0