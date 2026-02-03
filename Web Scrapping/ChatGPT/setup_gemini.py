"""
Interactive setup for FREE Google Gemini API
"""
import os
import webbrowser

print("="*60)
print("🆓 FREE AI Setup - Google Gemini")
print("="*60)

print("\n📝 Step 1: Get your FREE Gemini API Key")
print("\nI'll open the Google AI Studio page for you...")
print("(If it doesn't open, go to: https://makersuite.google.com/app/apikey)")

input("\nPress ENTER to open the browser...")

# Open the API key page
webbrowser.open("https://makersuite.google.com/app/apikey")

print("\n" + "="*60)
print("📋 Follow these steps in your browser:")
print("="*60)
print("\n1. Sign in with your Google account")
print("2. Click 'Create API key'")
print("3. Click 'Create API key in new project'")
print("4. Copy the API key")
print("\n" + "="*60)

# Get the API key from user
print("\n✏️ Step 2: Paste your API key here")
api_key = input("\nPaste your Gemini API key: ").strip()

if not api_key:
    print("\n❌ No API key provided. Exiting...")
    exit(1)

# Read existing .env file
env_file = ".env"
env_content = ""

if os.path.exists(env_file):
    with open(env_file, "r") as f:
        env_content = f.read()

# Update or add GEMINI_API_KEY
if "GEMINI_API_KEY=" in env_content:
    # Replace existing key
    lines = env_content.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("GEMINI_API_KEY="):
            new_lines.append(f"GEMINI_API_KEY={api_key}")
        else:
            new_lines.append(line)
    env_content = "\n".join(new_lines)
else:
    # Add new key
    if not env_content.endswith("\n"):
        env_content += "\n"
    env_content += f"\n# Google Gemini API (FREE)\nGEMINI_API_KEY={api_key}\n"

# Write back to .env
with open(env_file, "w") as f:
    f.write(env_content)

print("\n✅ API key saved to .env file!")

# Test the connection
print("\n🔍 Step 3: Testing connection...")
print("\nTesting your Gemini API key...")

import requests
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

try:
    test_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Say 'Hello! Setup successful!' in 5 words."}]
        }]
    }
    
    response = requests.post(test_url, json=payload, timeout=10, verify=False)
    
    if response.status_code == 200:
        result = response.json()
        message = result['candidates'][0]['content']['parts'][0]['text']
        print(f"\n✅ SUCCESS! Gemini responded: {message}")
        print("\n" + "="*60)
        print("🎉 Setup Complete!")
        print("="*60)
        print("\n📝 You can now run:")
        print("   python v2_gemini_free.py")
        print("\n💡 Benefits:")
        print("   • 60 requests per minute")
        print("   • 1,500 requests per day")
        print("   • Completely FREE!")
        print("   • No credit card required")
        print("\n" + "="*60)
    else:
        print(f"\n❌ Test failed: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        print("\nPlease check your API key and try again.")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPlease check your internet connection and try again.")


