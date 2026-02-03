# backend/routes/oni_api.py
# ONI API endpoints with automatic token management

from flask import Blueprint, request, jsonify
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

oni_api_bp = Blueprint('oni_api', __name__)

# ONI Configuration
ONI_CONFIG = {
    'token_url': 'https://login-itg2.oracleoutsourcing.com/oam/oauth2/oauthservice/token',
    'api_url': 'https://dxhub-api-itg2.comcast.com/ccm/graphql',
    'client_id': 'ff7d1a46c93e40e0b3e330ee15f83a40',
    'client_secret': '59eea25c-60be-423e-9ec5-58cbb42dce6b',
    'scope': 'ComcastCCM.Search'
}

def get_oni_token():
    """Get ONI authentication token"""
    try:
        response = requests.post(
            ONI_CONFIG['token_url'],
            data={
                'grant_type': 'client_credentials',
                'client_id': ONI_CONFIG['client_id'],
                'client_secret': ONI_CONFIG['client_secret'],
                'scope': ONI_CONFIG['scope']
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            verify=False,
            timeout=30
        )
        if response.ok:
            return response.json().get('access_token')
        return None
    except Exception as e:
        print(f"ONI Token Error: {e}")
        return None

def execute_graphql_query(query, variables=None):
    """Execute GraphQL query against ONI API"""
    token = get_oni_token()
    if not token:
        return {'success': False, 'error': 'Failed to get ONI token'}
    
    try:
        payload = {'query': query}
        if variables:
            payload['variables'] = variables
        
        response = requests.post(
            ONI_CONFIG['api_url'],
            json=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            verify=False,
            timeout=60
        )
        
        return {
            'success': response.ok,
            'status_code': response.status_code,
            'data': response.json() if response.ok else None,
            'error': response.text if not response.ok else None
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

@oni_api_bp.route('/status', methods=['GET'])
def check_status():
    """Check ONI API connectivity"""
    token = get_oni_token()
    return jsonify({
        'connected': token is not None,
        'service': 'ONI API',
        'endpoint': ONI_CONFIG['api_url']
    })

@oni_api_bp.route('/find-by-customer-id', methods=['POST'])
def find_by_customer_id():
    """Search by Customer ID"""
    data = request.get_json()
    customer_id = data.get('customerId', '')
    
    if not customer_id:
        return jsonify({'success': False, 'error': 'Customer ID is required'}), 400
    
    query = '''
    query SearchByCustomerId($customerId: String!) {
        searchProducts(
            searchCriteria: {
                properties: [
                    { name: "customerId", value: $customerId }
                ]
            }
        ) {
            id
            name
            status
            customerId
            siteId
            externalId {
                id
                system
            }
            characteristics {
                name
                value
            }
        }
    }
    '''
    
    result = execute_graphql_query(query, {'customerId': customer_id})
    return jsonify(result)

@oni_api_bp.route('/find-by-external-service-id', methods=['POST'])
def find_by_external_service_id():
    """Search by External Service ID"""
    data = request.get_json()
    external_id = data.get('externalServiceId', '')
    system_id = data.get('externalSystemId', 'SOM')
    
    if not external_id:
        return jsonify({'success': False, 'error': 'External Service ID is required'}), 400
    
    query = '''
    query SearchByExternalId($externalId: String!, $systemId: String!) {
        searchProducts(
            searchCriteria: {
                properties: [
                    { name: "externalId.id", value: $externalId },
                    { name: "externalId.system", value: $systemId }
                ]
            }
        ) {
            id
            name
            status
            customerId
            siteId
            externalId {
                id
                system
            }
            characteristics {
                name
                value
            }
        }
    }
    '''
    
    result = execute_graphql_query(query, {'externalId': external_id, 'systemId': system_id})
    return jsonify(result)

@oni_api_bp.route('/find-by-product-id', methods=['POST'])
def find_by_product_id():
    """Search by Product ID"""
    data = request.get_json()
    product_id = data.get('productId', '')
    
    if not product_id:
        return jsonify({'success': False, 'error': 'Product ID is required'}), 400
    
    query = '''
    query SearchByProductId($productId: String!) {
        searchProducts(
            searchCriteria: {
                properties: [
                    { name: "id", value: $productId }
                ]
            }
        ) {
            id
            name
            status
            customerId
            siteId
            externalId {
                id
                system
            }
            characteristics {
                name
                value
            }
            relatedProducts {
                id
                name
                relationshipType
            }
        }
    }
    '''
    
    result = execute_graphql_query(query, {'productId': product_id})
    return jsonify(result)

@oni_api_bp.route('/find-by-site-id', methods=['POST'])
def find_by_site_id():
    """Search by Site ID"""
    data = request.get_json()
    site_id = data.get('siteId', '')
    
    if not site_id:
        return jsonify({'success': False, 'error': 'Site ID is required'}), 400
    
    query = '''
    query SearchBySiteId($siteId: String!) {
        searchProducts(
            searchCriteria: {
                properties: [
                    { name: "siteId", value: $siteId }
                ]
            }
        ) {
            id
            name
            status
            customerId
            siteId
            externalId {
                id
                system
            }
            characteristics {
                name
                value
            }
        }
    }
    '''
    
    result = execute_graphql_query(query, {'siteId': site_id})
    return jsonify(result)

@oni_api_bp.route('/custom-query', methods=['POST'])
def custom_query():
    """Execute custom GraphQL query"""
    data = request.get_json()
    properties = data.get('properties', [])
    
    if not properties:
        return jsonify({'success': False, 'error': 'Query properties are required'}), 400
    
    # Build dynamic property list
    property_str = ', '.join([
        f'{{ name: "{p.get("name", "")}", value: "{p.get("value", "")}" }}'
        for p in properties
    ])
    
    query = f'''
    query CustomSearch {{
        searchProducts(
            searchCriteria: {{
                properties: [{property_str}]
            }}
        ) {{
            id
            name
            status
            customerId
            siteId
            externalId {{
                id
                system
            }}
            characteristics {{
                name
                value
            }}
        }}
    }}
    '''
    
    result = execute_graphql_query(query)
    return jsonify(result)
