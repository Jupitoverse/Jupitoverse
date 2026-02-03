# backend/routes/activity_data.py
"""Activity Data Routes - Loads and serves OSO activity data from JSON (fast loading)"""

from flask import Blueprint, jsonify, request
import json
import os
from pathlib import Path

activity_data_bp = Blueprint('activity_data', __name__)

# Cache for activity data
_activity_data_cache = None

def get_json_path():
    """Get the path to the JSON file"""
    # Try multiple possible locations
    script_dir = Path(__file__).parent
    possible_paths = [
        script_dir / 'data' / 'oso_activity_data.json',
        Path(r'C:\Users\abhisha3\Desktop\Projects\DOX\Orion-Agent\Orionverse\backend\data\oso_activity_data.json'),
        Path(r'C:\Users\abhisha3\Desktop\Projects\DOX\Orion-Agent\Orionverse\OSO_activity_data (1).xlsx').parent / 'backend' / 'data' / 'oso_activity_data.json',
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    return None

def get_excel_path():
    """Get the path to the Excel file (fallback)"""
    possible_paths = [
        r'C:\Users\abhisha3\Desktop\Projects\DOX\Orion-Agent\Orionverse\OSO_activity_data (1).xlsx',
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'OSO_activity_data (1).xlsx'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return possible_paths[0] if possible_paths else None

def load_activity_data():
    """Load activity data from JSON file (fast) or Excel (fallback)"""
    global _activity_data_cache
    
    if _activity_data_cache is not None:
        return _activity_data_cache
    
    # Try to load from JSON first (much faster)
    json_path = get_json_path()
    if json_path and os.path.exists(json_path):
        try:
            print(f"[INFO] Loading activity data from JSON: {json_path}")
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            _activity_data_cache = {
                'columns': data.get('columns', []),
                'data': data.get('data', []),
                'total_rows': data.get('total_rows', len(data.get('data', [])))
            }
            
            print(f"[INFO] Successfully loaded {_activity_data_cache['total_rows']} records from JSON")
            return _activity_data_cache
        except Exception as e:
            print(f"[WARN] Failed to load from JSON: {str(e)}, trying Excel fallback...")
    
    # Fallback to Excel if JSON doesn't exist
    try:
        import pandas as pd
        excel_path = get_excel_path()
        if not excel_path or not os.path.exists(excel_path):
            error_msg = f"Neither JSON nor Excel file found. Please run convert_excel_to_json.py first."
            print(f"[ERROR] {error_msg}")
            return {'columns': [], 'data': [], 'total_rows': 0, 'error': error_msg}
        
        print(f"[INFO] Loading activity data from Excel (slow): {excel_path}")
        print(f"[INFO] Consider running scripts/convert_excel_to_json.py for faster loading")
        
        try:
            df = pd.read_excel(excel_path, engine='openpyxl')
        except Exception as e:
            print(f"[WARN] openpyxl failed, trying default engine: {str(e)}")
            df = pd.read_excel(excel_path)
        
        df.columns = [str(col).strip() for col in df.columns]
        df = df.fillna('')
        
        _activity_data_cache = {
            'columns': list(df.columns),
            'data': df.to_dict('records'),
            'total_rows': len(df)
        }
        
        print(f"[INFO] Successfully loaded {len(df)} activity records from Excel")
        return _activity_data_cache
        
    except Exception as e:
        error_msg = f"Failed to load activity data: {str(e)}"
        print(f"[ERROR] {error_msg}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return {'columns': [], 'data': [], 'total_rows': 0, 'error': error_msg}

@activity_data_bp.route('/all', methods=['GET'])
def get_all_activity_data():
    """Get all activity data"""
    data = load_activity_data()
    return jsonify(data)

@activity_data_bp.route('/columns', methods=['GET'])
def get_columns():
    """Get column names"""
    data = load_activity_data()
    return jsonify({'columns': data.get('columns', [])})

@activity_data_bp.route('/search', methods=['POST'])
def search_activity_data():
    """Search activity data with filters"""
    try:
        request_data = request.get_json() or {}
        search_term = request_data.get('search', '').lower()
        column_filters = request_data.get('columnFilters', {})
        sort_column = request_data.get('sortColumn', '')
        sort_direction = request_data.get('sortDirection', 'asc')
        page = request_data.get('page', 1)
        page_size = request_data.get('pageSize', 100)
        
        data = load_activity_data()
        records = data.get('data', [])
        
        # Apply global search
        if search_term:
            records = [
                row for row in records
                if any(search_term in str(value).lower() for value in row.values())
            ]
        
        # Apply column-specific filters
        for column, filter_value in column_filters.items():
            if filter_value:
                filter_value_lower = filter_value.lower()
                records = [
                    row for row in records
                    if filter_value_lower in str(row.get(column, '')).lower()
                ]
        
        # Apply sorting
        if sort_column and sort_column in data.get('columns', []):
            records = sorted(
                records,
                key=lambda x: str(x.get(sort_column, '')).lower(),
                reverse=(sort_direction == 'desc')
            )
        
        # Pagination
        total_filtered = len(records)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_records = records[start_idx:end_idx]
        
        return jsonify({
            'columns': data.get('columns', []),
            'data': paginated_records,
            'total_rows': total_filtered,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_filtered + page_size - 1) // page_size
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activity_data_bp.route('/status', methods=['GET'])
def get_status():
    """Check if data is loaded and ready"""
    global _activity_data_cache
    if _activity_data_cache is not None:
        return jsonify({
            'loaded': True,
            'total_records': _activity_data_cache.get('total_rows', 0),
            'columns': len(_activity_data_cache.get('columns', []))
        })
    else:
        json_path = get_json_path()
        excel_path = get_excel_path()
        json_exists = json_path and os.path.exists(json_path)
        excel_exists = excel_path and os.path.exists(excel_path)
        return jsonify({
            'loaded': False,
            'json_exists': json_exists,
            'json_path': json_path,
            'excel_exists': excel_exists,
            'excel_path': excel_path
        })

@activity_data_bp.route('/refresh', methods=['POST'])
def refresh_data():
    """Force refresh of activity data from Excel"""
    global _activity_data_cache
    _activity_data_cache = None
    data = load_activity_data()
    if data.get('error'):
        return jsonify({
            'success': False,
            'error': data.get('error')
        }), 500
    return jsonify({
        'success': True,
        'message': f'Refreshed {data.get("total_rows", 0)} records'
    })

@activity_data_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about the activity data"""
    try:
        data = load_activity_data()
        
        # Check if there was an error loading
        if data.get('error'):
            return jsonify({
                'error': data.get('error'),
                'total_records': 0,
                'columns': 0,
                'unique_interfaces': 0,
                'unique_profiles': 0,
                'unique_implementations': 0
            }), 500
        
        records = data.get('data', [])
        
        # Get unique values for key columns
        stats = {
            'total_records': len(records),
            'columns': len(data.get('columns', [])),
            'unique_interfaces': len(set(str(r.get('interface', '')) for r in records if r.get('interface'))),
            'unique_profiles': len(set(str(r.get('profile', '')) for r in records if r.get('profile'))),
            'unique_implementations': len(set(str(r.get('implementation', '')) for r in records if r.get('implementation'))),
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
