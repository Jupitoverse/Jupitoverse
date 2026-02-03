"""
Diagnostic tool to test OpenAI API connection
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("=" * 60)
print("🔧 OpenAI API Connection Diagnostics")
print("=" * 60)

# 1. Check API Key
print("\n1️⃣ Checking API Key...")
if OPENAI_API_KEY:
    # Mask the key for security
    masked_key = OPENAI_API_KEY[:10] + "..." + OPENAI_API_KEY[-4:]
    print(f"   ✅ API Key found: {masked_key}")
    print(f"   Length: {len(OPENAI_API_KEY)} characters")
    if OPENAI_API_KEY.startswith("sk-"):
        print("   ✅ Key format looks valid (starts with 'sk-')")
    else:
        print("   ⚠️ Key format may be invalid (should start with 'sk-')")
else:
    print("   ❌ API Key not found!")
    exit(1)

# 2. Test general internet connectivity
print("\n2️⃣ Testing internet connectivity...")
try:
    response = requests.get("https://www.google.com", timeout=5)
    print(f"   ✅ Internet connection OK (Status: {response.status_code})")
except Exception as e:
    print(f"   ❌ Internet connection failed: {e}")
    print("   💡 Check your network connection")

# 3. Test OpenAI API endpoint connectivity
print("\n3️⃣ Testing OpenAI API endpoint...")
try:
    response = requests.get("https://api.openai.com", timeout=10)
    print(f"   ✅ Can reach api.openai.com (Status: {response.status_code})")
except requests.exceptions.ProxyError:
    print("   ❌ Proxy error - you may be behind a corporate proxy")
    print("   💡 Try setting HTTP_PROXY and HTTPS_PROXY environment variables")
except requests.exceptions.SSLError:
    print("   ❌ SSL certificate error")
    print("   💡 Your network may be intercepting SSL connections")
except Exception as e:
    print(f"   ❌ Cannot reach api.openai.com: {type(e).__name__}: {e}")
    print("   💡 You may be behind a firewall")

# 4. Test OpenAI API authentication
print("\n4️⃣ Testing OpenAI API authentication...")
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

try:
    # Try to list models (lightweight endpoint)
    response = requests.get(
        "https://api.openai.com/v1/models",
        headers=headers,
        timeout=15
    )
    
    if response.status_code == 200:
        print("   ✅ API authentication successful!")
        models = response.json()
        print(f"   ✅ Found {len(models.get('data', []))} models available")
        print("\n   📋 Some available models:")
        for model in models.get('data', [])[:5]:
            print(f"      - {model.get('id')}")
    elif response.status_code == 401:
        print("   ❌ Authentication failed (401 Unauthorized)")
        print("   💡 Your API key may be invalid or expired")
        print("   💡 Check: https://platform.openai.com/api-keys")
    elif response.status_code == 429:
        print("   ⚠️ Rate limit or quota exceeded (429)")
        print("   💡 Check your usage at: https://platform.openai.com/usage")
    else:
        print(f"   ❌ API returned status code: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
except requests.exceptions.ProxyError:
    print("   ❌ Proxy error during API call")
    print("   💡 Configure proxy settings if needed")
except requests.exceptions.SSLError as e:
    print(f"   ❌ SSL Error: {e}")
    print("   💡 Try: pip install --upgrade certifi")
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

# 5. Test with a simple ChatGPT request
print("\n5️⃣ Testing ChatGPT API...")
try:
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Say 'test successful' in 2 words"}],
            "max_tokens": 10
        },
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        message = result['choices'][0]['message']['content']
        print(f"   ✅ ChatGPT API working!")
        print(f"   📝 Response: {message}")
    else:
        print(f"   ❌ ChatGPT API failed (Status: {response.status_code})")
        print(f"   Response: {response.text[:200]}")
        
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("✅ Diagnostics complete!")
print("=" * 60)


