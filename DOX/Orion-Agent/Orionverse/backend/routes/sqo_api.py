# backend/routes/sqo_api.py
"""SQO API Routes - Handles all SQO domain API calls with automatic token management"""

from flask import Blueprint, request, jsonify
import requests
import json

sqo_api_bp = Blueprint('sqo_api', __name__)

# SQO Configuration
SQO_CONFIG = {
    'login_url': 'https://sqo.orion.comcast.com/securitymanagement-ms/v1/Login',
    'odo_login_url': 'https://sqoapp.orion.comcast.com:443/securitymanagement-ms/Login',
    'billing_url': 'https://sqo.orion.comcast.com/prod-delivery-ms/product-delivery/v1/products-billing-request',
    'delivery_url': 'https://sqo.orion.comcast.com/frameworkagreement-ms/framework-agreement-management/v1/delivery-request',
    'product_status_url': 'https://sqo.orion.comcast.com/prod-delivery-ms/product-delivery/v1/products-assignment-request',
    'fulfillment_url': 'https://sqoapp.orion.comcast.com:443/prod-delivery-ms/product-delivery/v1/products-fulfillment-request',
    'quote_alignment_base_url': 'https://sqoapp.orion.comcast.com:443/product_quote_aligner-ms/product_quote_aligner-ms-management/v1/framework-agreement',
    'default_credentials': {
        'user': 'ODOUser',
        'password': 'Unix11'
    }
}

# Store tokens in memory (in production, use proper session management)
token_cache = {
    'sqo_token': None,
    'odo_token': None
}

def get_sqo_token():
    """Get SQO token, fetching new one if needed"""
    try:
        payload = json.dumps(SQO_CONFIG['default_credentials'])
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(
            SQO_CONFIG['login_url'],
            headers=headers,
            data=payload,
            timeout=30,
            verify=False
        )
        
        if response.status_code == 200:
            data = response.json()
            token_cache['sqo_token'] = data.get('token') or data.get('access_token') or data.get('sessionToken')
            return token_cache['sqo_token'], None
        else:
            return None, f"Login failed: {response.status_code} - {response.text}"
    except Exception as e:
        return None, str(e)

def get_odo_token():
    """Get ODO token"""
    try:
        payload = json.dumps(SQO_CONFIG['default_credentials'])
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(
            SQO_CONFIG['odo_login_url'],
            headers=headers,
            data=payload,
            timeout=30,
            verify=False
        )
        
        if response.status_code == 200:
            data = response.json()
            token_cache['odo_token'] = data.get('token') or data.get('access_token') or data.get('sessionToken')
            return token_cache['odo_token'], None
        else:
            return None, f"Login failed: {response.status_code} - {response.text}"
    except Exception as e:
        return None, str(e)

@sqo_api_bp.route('/status', methods=['GET'])
def get_status():
    """Check SQO API service status"""
    return jsonify({
        'status': 'online',
        'service': 'SQO API',
        'endpoints': [
            'billing-manual',
            'submit-delivery',
            'set-product-status',
            'send-fulfillment',
            'quote-alignment'
        ]
    })

@sqo_api_bp.route('/billing-manual', methods=['POST'])
def billing_manual_call():
    """Execute Billing Manual Call API"""
    try:
        data = request.get_json()
        
        # Get fresh token
        token, error = get_sqo_token()
        if error:
            return jsonify({'success': False, 'error': f'Token Error: {error}'}), 401
        
        # Build payload
        payload = {
            "correlationId": data.get('correlationId', ''),
            "resend": data.get('resend', False),
            "products": data.get('products', [])
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            SQO_CONFIG['billing_url'],
            headers=headers,
            json=payload,
            timeout=60,
            verify=False
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {'raw_response': response.text}
        
        return jsonify({
            'success': response.status_code in [200, 201, 202],
            'status_code': response.status_code,
            'data': response_data,
            'request_payload': payload
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sqo_api_bp.route('/submit-delivery', methods=['POST'])
def submit_to_delivery():
    """Execute Submit to Delivery API"""
    try:
        data = request.get_json()
        
        # Get fresh token
        token, error = get_sqo_token()
        if error:
            return jsonify({'success': False, 'error': f'Token Error: {error}'}), 401
        
        # Build payload
        payload = {
            "correlationId": data.get('correlationId', ''),
            "frameworkAgreementRef": data.get('frameworkAgreementRef', {}),
            "productAgreementItems": data.get('productAgreementItems', [])
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            SQO_CONFIG['delivery_url'],
            headers=headers,
            json=payload,
            timeout=60,
            verify=False
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {'raw_response': response.text}
        
        return jsonify({
            'success': response.status_code in [200, 201, 202],
            'status_code': response.status_code,
            'data': response_data,
            'request_payload': payload
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sqo_api_bp.route('/set-product-status', methods=['POST'])
def set_product_status():
    """Execute Set Product Status API"""
    try:
        data = request.get_json()
        
        # Get fresh token
        token, error = get_odo_token()
        if error:
            return jsonify({'success': False, 'error': f'Token Error: {error}'}), 401
        
        # Build payload
        payload = {
            "products": data.get('products', []),
            "correlationId": data.get('correlationId', '')
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            SQO_CONFIG['product_status_url'],
            headers=headers,
            json=payload,
            timeout=60,
            verify=False
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {'raw_response': response.text}
        
        return jsonify({
            'success': response.status_code in [200, 201, 202],
            'status_code': response.status_code,
            'data': response_data,
            'request_payload': payload
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sqo_api_bp.route('/send-fulfillment', methods=['POST'])
def send_to_fulfillment():
    """Execute Send to Fulfillment API"""
    try:
        data = request.get_json()
        
        # Get fresh token
        token, error = get_odo_token()
        if error:
            return jsonify({'success': False, 'error': f'Token Error: {error}'}), 401
        
        # Build payload
        payload = {
            "products": data.get('products', []),
            "correlationId": data.get('correlationId', ''),
            "fulfillmentGroupId": data.get('fulfillmentGroupId', ''),
            "fulfillmentGroupAction": data.get('fulfillmentGroupAction', 'CREATE'),
            "fulfillmentGroupVersion": data.get('fulfillmentGroupVersion', '1')
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            SQO_CONFIG['fulfillment_url'],
            headers=headers,
            json=payload,
            timeout=60,
            verify=False
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {'raw_response': response.text}
        
        return jsonify({
            'success': response.status_code in [200, 201, 202],
            'status_code': response.status_code,
            'data': response_data,
            'request_payload': payload
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sqo_api_bp.route('/quote-alignment', methods=['POST'])
def quote_alignment():
    """Execute Quote Alignment API"""
    try:
        data = request.get_json()
        
        # Get fresh token
        token, error = get_odo_token()
        if error:
            return jsonify({'success': False, 'error': f'Token Error: {error}'}), 401
        
        framework_agreement_id = data.get('frameworkAgreementId', '')
        request_type = data.get('requestType', 'Quote')
        
        url = f"{SQO_CONFIG['quote_alignment_base_url']}/{framework_agreement_id}/align-quote"
        
        payload = {
            "requestType": request_type
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60,
            verify=False
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {'raw_response': response.text}
        
        return jsonify({
            'success': response.status_code in [200, 201, 202],
            'status_code': response.status_code,
            'data': response_data,
            'request_payload': payload,
            'request_url': url
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
