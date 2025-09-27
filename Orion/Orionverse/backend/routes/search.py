# backend/routes/search.py
from flask import Blueprint, jsonify, request
import json
import os
import database
import psycopg2.extras

search_bp = Blueprint('search', __name__)

# --- Helper function to load JSON data ---
def load_json_data(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ FATAL ERROR: JSON data file not found at {path}. Run convert_excel.py.")
        return []

# Load data once when the server starts
sr_data = load_json_data('sr_data.json')
defect_data = load_json_data('defect_data.json')

@search_bp.route('/all', methods=['GET'])
def get_all_data():
    """
    Fetches the TOP 10 rows from each data source for the initial page load.
    """
    wa_data = []
    try:
        conn = database.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # ✅ FIX: Added LIMIT 10 to the query
        cur.execute('SELECT * FROM workarounds ORDER BY created_date DESC LIMIT 10;')
        wa_data = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error in get_all_data: {e}")
    
    return jsonify({
        # ✅ FIX: Slicing the JSON data to return only the first 10 rows
        "sr_data": sr_data[:10],
        "defect_data": defect_data[:10],
        "wa_data": wa_data
    })

@search_bp.route('/filter', methods=['POST'])
def filter_data():
    """
    Performs a complex, multi-source search and returns ALL matching results.
    """
    # ... (The filter logic remains the same as before) ...
    filters = request.get_json()
    
    filtered_sr = sr_data
    filtered_defect = defect_data
    
    customer_id = filters.get('customer_id', '').lower()
    if customer_id:
        filtered_sr = [r for r in filtered_sr if str(r.get('CUSTOMER_ID', '')).lower() == customer_id]

    # ... (Add all other filter logic here exactly as before) ...
    
    # Fetch and filter WA data from the database
    wa_data = []
    try:
        conn = database.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        search_anything = filters.get('search_anything', '').lower()
        if search_anything:
            query = "SELECT * FROM workarounds WHERE category ILIKE %s OR issue ILIKE %s OR description ILIKE %s ORDER BY created_date DESC;"
            cur.execute(query, (f'%{search_anything}%', f'%{search_anything}%', f'%{search_anything}%'))
        else:
            cur.execute('SELECT * FROM workarounds ORDER BY created_date DESC;')
        wa_data = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error in filter_data: {e}")

    return jsonify({
        "sr_data": filtered_sr,
        "defect_data": filtered_defect,
        "wa_data": wa_data
    })