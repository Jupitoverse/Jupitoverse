# backend/routes/oni_api.py
"""ONI API Routes - Handles all ONI domain API calls with automatic token management"""

from flask import Blueprint, request, jsonify
import requests
import json

oni_api_bp = Blueprint('oni_api', __name__)

# ONI Configuration
ONI_CONFIG = {
    'token_url': 'https://oso.orion.comcast.com/dop/security/rest/loginservice/login',
    'find_cross_context_url': 'https://oni.orion.comcast.com/servo/api/service/findcrosscontext',
    'default_credentials': {
        'userID': 'nap-admin-user',
        'password': 'Nap-admin-user1'
    }
}

# Store token in memory
token_cache = {
    'oni_token': None
}

def get_oni_token():
    """Get ONI token, fetching new one if needed"""
    try:
        payload = json.dumps(ONI_CONFIG['default_credentials'])
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(
            ONI_CONFIG['token_url'],
            headers=headers,
            data=payload,
            timeout=30,
            verify=False
        )
        
        if response.status_code == 200:
            data = response.json()
            # ONI returns token in different formats
            token_cache['oni_token'] = (
                data.get('token') or 
                data.get('access_token') or 
                data.get('sessionToken') or
                data.get('UEM')
            )
            return token_cache['oni_token'], None
        else:
            return None, f"Login failed: {response.status_code} - {response.text}"
    except Exception as e:
        return None, str(e)

@oni_api_bp.route('/status', methods=['GET'])
def get_status():
    """Check ONI API service status"""
    return jsonify({
        'status': 'online',
        'service': 'ONI API',
        'endpoints': [
            'find-by-customer-id',
            'find-by-external-service-id',
            'find-by-product-id',
            'find-by-site-id'
        ]
    })

def make_find_request(criteria_properties):
    """Common function to make findcrosscontext requests"""
    # Get fresh token
    token, error = get_oni_token()
    if error:
        return {'success': False, 'error': f'Token Error: {error}'}, 401
    
    payload = {
        "retrievalBehaviour": {
            "limit": 1000,
            "returnRelatedObjects": True,
            "historyLevel": None,
            "valid": True
        },
        "criteria": [
            {
                "properties": criteria_properties
            }
        ]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.post(
            ONI_CONFIG['find_cross_context_url'],
            headers=headers,
            json=payload,
            timeout=60,
            verify=False
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {'raw_response': response.text}
        
        return {
            'success': response.status_code in [200, 201, 202],
            'status_code': response.status_code,
            'data': response_data,
            'request_payload': payload
        }, response.status_code
        
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500

@oni_api_bp.route('/find-by-customer-id', methods=['POST'])
def find_by_customer_id():
    """Find services by Customer ID"""
    try:
        data = request.get_json()
        customer_id = data.get('customerId', '')
        
        if not customer_id:
            return jsonify({'success': False, 'error': 'Customer ID is required'}), 400
        
        criteria_properties = [
            {
                "name": "serviceCharacteristic.customerId",
                "op": "eq",
                "value": customer_id,
                "valid": True
            }
        ]
        
        result, status_code = make_find_request(criteria_properties)
        return jsonify(result), status_code if not result.get('success') else 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@oni_api_bp.route('/find-by-external-service-id', methods=['POST'])
def find_by_external_service_id():
    """Find services by External Service ID"""
    try:
        data = request.get_json()
        external_service_id = data.get('externalServiceId', '')
        external_system_id = data.get('externalSystemId', 'SOM')
        
        if not external_service_id:
            return jsonify({'success': False, 'error': 'External Service ID is required'}), 400
        
        criteria_properties = [
            {
                "name": "externalServiceId",
                "op": "eq",
                "value": external_service_id
            },
            {
                "name": "externalSystemId",
                "op": "eq",
                "value": external_system_id
            }
        ]
        
        result, status_code = make_find_request(criteria_properties)
        return jsonify(result), status_code if not result.get('success') else 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@oni_api_bp.route('/find-by-product-id', methods=['POST'])
def find_by_product_id():
    """Find services by Product ID"""
    try:
        data = request.get_json()
        product_id = data.get('productId', '')
        
        if not product_id:
            return jsonify({'success': False, 'error': 'Product ID is required'}), 400
        
        criteria_properties = [
            {
                "name": "serviceCharacteristic.productInstanceId",
                "op": "eq",
                "value": product_id
            }
        ]
        
        result, status_code = make_find_request(criteria_properties)
        return jsonify(result), status_code if not result.get('success') else 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@oni_api_bp.route('/find-by-site-id', methods=['POST'])
def find_by_site_id():
    """Find services by Site ID"""
    try:
        data = request.get_json()
        site_id = data.get('siteId', '')
        
        if not site_id:
            return jsonify({'success': False, 'error': 'Site ID is required'}), 400
        
        criteria_properties = [
            {
                "name": "serviceCharacteristic.siteId",
                "op": "eq",
                "value": site_id
            }
        ]
        
        result, status_code = make_find_request(criteria_properties)
        return jsonify(result), status_code if not result.get('success') else 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@oni_api_bp.route('/custom-query', methods=['POST'])
def custom_query():
    """Execute custom findcrosscontext query"""
    try:
        data = request.get_json()
        criteria_properties = data.get('properties', [])
        
        if not criteria_properties:
            return jsonify({'success': False, 'error': 'Query properties are required'}), 400
        
        result, status_code = make_find_request(criteria_properties)
        return jsonify(result), status_code if not result.get('success') else 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
