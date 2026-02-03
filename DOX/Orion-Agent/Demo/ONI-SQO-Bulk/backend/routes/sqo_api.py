# backend/routes/sqo_api.py
# SQO API endpoints with automatic token management

from flask import Blueprint, request, jsonify
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sqo_api_bp = Blueprint('sqo_api', __name__)

# SQO Configuration
SQO_CONFIG = {
    'login_url': 'https://xsqo-intg2.np.xtify.io/api/v1/login',
    'odo_login_url': 'https://xsqo-intg2.np.xtify.io/api/v1/odo/login',
    'base_url': 'https://xsqo-intg2.np.xtify.io/api/v1',
    'user': 'ODOUser',
    'password': 'Unix11'
}

def get_sqo_token():
    """Get SQO authentication token"""
    try:
        response = requests.post(
            SQO_CONFIG['login_url'],
            json={'user': SQO_CONFIG['user'], 'password': SQO_CONFIG['password']},
            headers={'Content-Type': 'application/json'},
            verify=False,
            timeout=30
        )
        if response.ok:
            data = response.json()
            return data.get('token') or data.get('access_token')
        return None
    except Exception as e:
        print(f"SQO Token Error: {e}")
        return None

def get_odo_token():
    """Get ODO authentication token"""
    try:
        response = requests.post(
            SQO_CONFIG['odo_login_url'],
            json={'user': SQO_CONFIG['user'], 'password': SQO_CONFIG['password']},
            headers={'Content-Type': 'application/json'},
            verify=False,
            timeout=30
        )
        if response.ok:
            data = response.json()
            return data.get('token') or data.get('access_token')
        return None
    except Exception as e:
        print(f"ODO Token Error: {e}")
        return None

@sqo_api_bp.route('/status', methods=['GET'])
def check_status():
    """Check SQO API connectivity"""
    token = get_sqo_token()
    return jsonify({
        'connected': token is not None,
        'service': 'SQO API',
        'endpoint': SQO_CONFIG['base_url']
    })

@sqo_api_bp.route('/billing-manual', methods=['POST'])
def billing_manual_call():
    """Execute Billing Manual Call"""
    try:
        token = get_odo_token()
        if not token:
            return jsonify({'success': False, 'error': 'Failed to get ODO token'}), 401
        
        data = request.get_json()
        
        payload = {
            "correlationId": data.get('correlationId', ''),
            "resend": data.get('resend', False),
            "products": data.get('products', [])
        }
        
        response = requests.post(
            f"{SQO_CONFIG['base_url']}/odo/billingManualCall",
            json=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            verify=False,
            timeout=60
        )
        
        return jsonify({
            'success': response.ok,
            'status_code': response.status_code,
            'data': response.json() if response.ok else None,
            'error': response.text if not response.ok else None
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sqo_api_bp.route('/submit-delivery', methods=['POST'])
def submit_to_delivery():
    """Submit to Delivery"""
    try:
        token = get_odo_token()
        if not token:
            return jsonify({'success': False, 'error': 'Failed to get ODO token'}), 401
        
        data = request.get_json()
        
        payload = {
            "correlationId": data.get('correlationId', ''),
            "frameworkAgreementRef": data.get('frameworkAgreementRef', {}),
            "productAgreementItems": data.get('productAgreementItems', [])
        }
        
        response = requests.post(
            f"{SQO_CONFIG['base_url']}/odo/submitToDelivery",
            json=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            verify=False,
            timeout=60
        )
        
        return jsonify({
            'success': response.ok,
            'status_code': response.status_code,
            'data': response.json() if response.ok else None,
            'error': response.text if not response.ok else None
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sqo_api_bp.route('/set-product-status', methods=['POST'])
def set_product_status():
    """Set Product Status"""
    try:
        token = get_odo_token()
        if not token:
            return jsonify({'success': False, 'error': 'Failed to get ODO token'}), 401
        
        data = request.get_json()
        
        payload = {
            "correlationId": data.get('correlationId', ''),
            "products": data.get('products', [])
        }
        
        response = requests.post(
            f"{SQO_CONFIG['base_url']}/odo/setProductStatus",
            json=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            verify=False,
            timeout=60
        )
        
        return jsonify({
            'success': response.ok,
            'status_code': response.status_code,
            'data': response.json() if response.ok else None,
            'error': response.text if not response.ok else None
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sqo_api_bp.route('/send-fulfillment', methods=['POST'])
def send_to_fulfillment():
    """Send to Fulfillment"""
    try:
        token = get_odo_token()
        if not token:
            return jsonify({'success': False, 'error': 'Failed to get ODO token'}), 401
        
        data = request.get_json()
        
        payload = {
            "correlationId": data.get('correlationId', ''),
            "fulfillmentGroupId": data.get('fulfillmentGroupId', ''),
            "fulfillmentGroupAction": data.get('fulfillmentGroupAction', 'CREATE'),
            "fulfillmentGroupVersion": data.get('fulfillmentGroupVersion', '1'),
            "products": data.get('products', [])
        }
        
        response = requests.post(
            f"{SQO_CONFIG['base_url']}/odo/sendToFulfillment",
            json=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            verify=False,
            timeout=60
        )
        
        return jsonify({
            'success': response.ok,
            'status_code': response.status_code,
            'data': response.json() if response.ok else None,
            'error': response.text if not response.ok else None
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@sqo_api_bp.route('/quote-alignment', methods=['POST'])
def quote_alignment():
    """Quote Alignment"""
    try:
        token = get_sqo_token()
        if not token:
            return jsonify({'success': False, 'error': 'Failed to get SQO token'}), 401
        
        data = request.get_json()
        
        fa_id = data.get('frameworkAgreementId', '')
        request_type = data.get('requestType', 'Quote')
        
        response = requests.get(
            f"{SQO_CONFIG['base_url']}/quoteAlignment/{fa_id}",
            params={'requestType': request_type},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            verify=False,
            timeout=60
        )
        
        return jsonify({
            'success': response.ok,
            'status_code': response.status_code,
            'data': response.json() if response.ok else None,
            'error': response.text if not response.ok else None
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
