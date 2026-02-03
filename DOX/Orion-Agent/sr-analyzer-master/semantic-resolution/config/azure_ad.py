"""
Azure AD Authentication Configuration
Configure Azure Active Directory for SSO login

NOTE: These are temporary credentials. Replace with production credentials before deployment.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if exists)
load_dotenv()

# Azure AD Configuration
# Credentials can be overridden via environment variables
AZURE_AD_CONFIG = {
    # Application (client) ID from Azure Portal
    "client_id": os.environ.get("AZURE_CLIENT_ID", "f81b1954-2ef9-44ad-950d-e26784f76453"),
    
    # Directory (tenant) ID from Azure Portal
    "tenant_id": os.environ.get("AZURE_TENANT_ID", "c8eca3ca-1276-46d5-9d9d-a0f2a028920f"),
    
    # Client secret (create in Azure Portal > Certificates & secrets)
    "client_secret": os.environ.get("AZURE_CLIENT_SECRET", "cGm8Q~EnAVizi5rPTlmjMFvdkY3R5L~Mc5l7FbQV"),
    
    # Redirect URI (must match Azure Portal configuration)
    # Default to HTTPS for Azure AD compliance (HTTP only allowed for localhost)
    "redirect_uri": os.environ.get("AZURE_REDIRECT_URI", "https://localhost:5000/auth/microsoft/callback"),
    
    # Authority URL
    "authority": f"https://login.microsoftonline.com/{os.environ.get('AZURE_TENANT_ID', 'c8eca3ca-1276-46d5-9d9d-a0f2a028920f')}",
    
    # Scopes for Microsoft Graph
    # Note: openid, profile, offline_access are automatically added by MSAL
    "scope": ["User.Read"],
}

# Graph API endpoint
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"


def is_azure_ad_configured() -> bool:
    """Check if Azure AD credentials are configured."""
    return bool(AZURE_AD_CONFIG.get("client_secret"))


def get_msal_app():
    """Create and return MSAL Confidential Client Application"""
    import msal
    
    return msal.ConfidentialClientApplication(
        AZURE_AD_CONFIG["client_id"],
        authority=AZURE_AD_CONFIG["authority"],
        client_credential=AZURE_AD_CONFIG["client_secret"],
    )


def get_auth_url(state=None):
    """Generate the Azure AD authorization URL"""
    msal_app = get_msal_app()
    
    auth_url = msal_app.get_authorization_request_url(
        scopes=AZURE_AD_CONFIG["scope"],
        redirect_uri=AZURE_AD_CONFIG["redirect_uri"],
        state=state,
    )
    
    return auth_url


def get_token_from_code(auth_code):
    """Exchange authorization code for access token"""
    msal_app = get_msal_app()
    
    result = msal_app.acquire_token_by_authorization_code(
        auth_code,
        scopes=AZURE_AD_CONFIG["scope"],
        redirect_uri=AZURE_AD_CONFIG["redirect_uri"],
    )
    
    return result


def get_user_info(access_token):
    """Get user information from Microsoft Graph API"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    response = requests.get(
        f"{GRAPH_API_ENDPOINT}/me",
        headers=headers,
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
