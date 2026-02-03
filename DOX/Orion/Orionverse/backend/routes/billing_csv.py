# backend/routes/billing_csv.py
from flask import Blueprint, jsonify, request
import csv
import os

billing_csv_bp = Blueprint('billing_csv', __name__)

@billing_csv_bp.route('/rebill-data', methods=['GET'])
def get_rebill_data():
    """
    Load and return Rebill 2025.csv data
    """
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Rebill 2025.csv')
        
        if not os.path.exists(csv_path):
            return jsonify({'error': 'CSV file not found'}), 404
        
        data = []
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        
        return jsonify({
            'success': True,
            'data': data,
            'total': len(data)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@billing_csv_bp.route('/rebill-data/search', methods=['POST'])
def search_rebill_data():
    """
    Search through Rebill data
    """
    try:
        search_params = request.json
        search_term = search_params.get('search', '').lower()
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Rebill 2025.csv')
        
        if not os.path.exists(csv_path):
            return jsonify({'error': 'CSV file not found'}), 404
        
        data = []
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Search across all fields
                if search_term:
                    row_str = ' '.join(str(v).lower() for v in row.values())
                    if search_term in row_str:
                        data.append(row)
                else:
                    data.append(row)
        
        return jsonify({
            'success': True,
            'data': data,
            'total': len(data)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



