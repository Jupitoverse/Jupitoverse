# backend/routes/excel_loader.py
from flask import Blueprint, jsonify, request
import pandas as pd
import json
import os

excel_loader_bp = Blueprint('excel_loader', __name__)

# Path to Excel files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

@excel_loader_bp.route('/sr-handling-data', methods=['GET'])
def get_sr_handling_data():
    """
    Load Ultron data from JSON file for SR Handling
    """
    try:
        json_path = os.path.join(BASE_DIR, 'backend', 'data', 'ultron_data.json')
        
        if not os.path.exists(json_path):
            return jsonify({'error': f'JSON file not found: {json_path}'}), 404
        
        # Read JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add Status and Assignee columns if they don't exist
        for record in data:
            if 'Status' not in record:
                record['Status'] = 'New'
            if 'Assignee' not in record:
                record['Assignee'] = ''
        
        # Get columns from first record
        columns = list(data[0].keys()) if data else []
        
        return jsonify({
            'success': True,
            'data': data,
            'total': len(data),
            'columns': columns
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@excel_loader_bp.route('/stuck-activities-data', methods=['GET'])
def get_stuck_activities_data():
    """
    Load Orion Outage Report data from JSON file for Stuck Activities
    Returns all sheets with their data
    """
    try:
        json_path = os.path.join(BASE_DIR, 'backend', 'data', 'outage_report_data.json')
        
        if not os.path.exists(json_path):
            return jsonify({'error': f'JSON file not found: {json_path}'}), 404
        
        # Read JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            sheets = json.load(f)
        
        sheets_data = {}
        for sheet_name, data in sheets.items():
            # Get columns from first record
            columns = list(data[0].keys()) if data else []
            
            sheets_data[sheet_name] = {
                'data': data,
                'columns': columns,
                'row_count': len(data)
            }
        
        return jsonify({
            'success': True,
            'sheets': sheets_data,
            'sheet_names': list(sheets.keys()),
            'total_sheets': len(sheets)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@excel_loader_bp.route('/sr-handling-update', methods=['POST'])
def update_sr_handling():
    """
    Update SR Handling data (Assignee and Status)
    In production, this should update a database
    For now, it returns success (data stored in localStorage on frontend)
    """
    try:
        data = request.get_json()
        # In production, save to database
        # For now, just acknowledge
        
        return jsonify({
            'success': True,
            'message': 'SR updated successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

