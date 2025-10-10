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
    Also returns total counts for statistics.
    """
    wa_data = []
    try:
        conn = database.get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT * FROM workarounds ORDER BY created_date DESC LIMIT 10;')
        wa_data = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error in get_all_data: {e}")
    
    print(f"📊 Initial load: {len(sr_data)} total SRs, {len(defect_data)} total defects, {len(wa_data)} WAs")
    print(f"📊 Returning 5 SRs, 5 Defects for initial display")
    
    return jsonify({
        "sr_data": sr_data[:5],  # Latest 5 SRs
        "defect_data": defect_data[:5],  # Latest 5 Defects
        "wa_data": wa_data,
        # Add total counts for statistics
        "total_counts": {
            "sr_total": len(sr_data),
            "defect_total": len(defect_data),
            "wa_total": len(wa_data)
        }
    })

@search_bp.route('/filter', methods=['POST'])
def filter_data():
    """
    Performs a complex, multi-source search and returns ALL matching results.
    Supports multiple filter criteria:
    - search_anything: Free text search across multiple fields
    - customer_id: Exact or partial match on Customer ID
    - osite_id: Site ID in format OSite_%_1
    - sr_id: Service Request ID
    - id: Defect ID
    """
    filters = request.get_json()
    print(f"\n{'='*60}")
    print(f"🔍 NEW SEARCH REQUEST")
    print(f"{'='*60}")
    print(f"Filters received: {filters}")
    print(f"Starting with {len(sr_data)} SRs and {len(defect_data)} Defects")
    
    # Start with all data
    filtered_sr = sr_data
    filtered_defect = defect_data
    
    # Extract filter values
    search_anything = filters.get('search_anything', '').strip().lower()
    customer_id = filters.get('customer_id', '').strip()
    osite_id = filters.get('osite_id', '').strip().lower()
    sr_id = filters.get('sr_id', '').strip().upper()
    defect_id = filters.get('id', '').strip()
    
    # Filter 1: Customer ID
    # SR → CUSTOMER_ID | Defect → Name, Description
    if customer_id:
        print(f"  Filtering by Customer ID: {customer_id}")
        filtered_sr = [
            r for r in filtered_sr 
            if str(r.get('CUSTOMER_ID', '')).lower().find(customer_id.lower()) != -1
        ]
        filtered_defect = [
            d for d in filtered_defect 
            if customer_id.lower() in str(d.get('Name', '')).lower() 
            or customer_id.lower() in str(d.get('Description', '')).lower()
        ]
    
    # Filter 2: OSite ID (format: OSite_%_1)
    # SR → DETAILS, UPDATE_DETAILS | Defect → Name, Description
    if osite_id:
        print(f"  Filtering by OSite ID: {osite_id}")
        filtered_sr = [
            r for r in filtered_sr 
            if osite_id in str(r.get('DETAILS', '')).lower() 
            or osite_id in str(r.get('UPDATE_DETAILS', '')).lower()
        ]
        filtered_defect = [
            d for d in filtered_defect 
            if osite_id in str(d.get('Name', '')).lower() 
            or osite_id in str(d.get('Description', '')).lower()
        ]
    
    # Filter 3: SR ID
    # SR → SR_ID | Defect → Name, Description
    if sr_id:
        print(f"  Filtering by SR ID: {sr_id}")
        filtered_sr = [
            r for r in filtered_sr 
            if sr_id in str(r.get('SR_ID', '')).upper()
        ]
        filtered_defect = [
            d for d in filtered_defect 
            if sr_id in str(d.get('Name', '')).upper() 
            or sr_id in str(d.get('Description', '')).upper()
        ]
    
    # Filter 4: Defect ID
    # SR → DETAILS, UPDATE_DETAILS | Defect → ID
    if defect_id:
        print(f"  Filtering by Defect ID: {defect_id}")
        filtered_sr = [
            r for r in filtered_sr 
            if defect_id in str(r.get('DETAILS', '')) 
            or defect_id in str(r.get('UPDATE_DETAILS', ''))
        ]
        filtered_defect = [
            d for d in filtered_defect 
            if str(d.get('ID', '')) == defect_id
        ]
    
    # Filter 5: Search Anything (free text)
    # SR → DETAILS, UPDATE_DETAILS | Defect → Name, Description
    if search_anything:
        print(f"  Filtering by Search Anything: {search_anything}")
        filtered_sr = [
            r for r in filtered_sr 
            if search_anything in str(r.get('DETAILS', '')).lower() 
            or search_anything in str(r.get('UPDATE_DETAILS', '')).lower()
        ]
        filtered_defect = [
            d for d in filtered_defect 
            if search_anything in str(d.get('Name', '')).lower() 
            or search_anything in str(d.get('Description', '')).lower()
        ]
    
    # Fetch and filter WA data from the database
    wa_data = []
    try:
        conn = database.get_db_connection()
        if not conn:
            print("❌ Database connection failed for WA data")
            wa_data = []
        else:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # If search_anything is provided, search in all WA fields
            if search_anything:
                query = """
                    SELECT * FROM workarounds 
                    WHERE LOWER(category) LIKE %s 
                       OR LOWER(issue) LIKE %s 
                       OR LOWER(description) LIKE %s 
                       OR LOWER(created_by) LIKE %s
                    ORDER BY created_date DESC;
                """
                search_pattern = f'%{search_anything}%'
                cur.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            else:
                # Return all workarounds if no search term
                cur.execute('SELECT * FROM workarounds ORDER BY created_date DESC;')
            
            wa_data = cur.fetchall()
            cur.close()
            conn.close()
            print(f"  Found {len(wa_data)} workarounds")
            
    except Exception as e:
        print(f"❌ Database error in filter_data: {e}")
        wa_data = []

    result_counts = {
        "sr_count": len(filtered_sr),
        "defect_count": len(filtered_defect),
        "wa_count": len(wa_data)
    }
    print(f"{'='*60}")
    print(f"✅ SEARCH COMPLETE")
    print(f"{'='*60}")
    print(f"Results: {result_counts}")
    if len(filtered_defect) > 0:
        print(f"Sample defect found: {filtered_defect[0].get('ID')} - {filtered_defect[0].get('Name')[:50]}...")
    else:
        print(f"⚠️ No defects found! Original defect_data had {len(defect_data)} records")
    print(f"{'='*60}\n")

    return jsonify({
        "sr_data": filtered_sr,
        "defect_data": filtered_defect,
        "wa_data": wa_data
    })