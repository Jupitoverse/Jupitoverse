"""
Web scraping with Google Gemini AI - FREE VERSION
Uses Google's Gemini API which has a generous free tier!
"""
import os
import requests
import warnings
from dotenv import load_dotenv

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Load environment variables
load_dotenv()

# Get API key (you'll need a Gemini API key)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("⚠️ GEMINI_API_KEY not found in .env file!")
    print("\n📝 To get a FREE Gemini API key:")
    print("   1. Go to: https://makersuite.google.com/app/apikey")
    print("   2. Click 'Create API Key'")
    print("   3. Add it to your .env file as: GEMINI_API_KEY=your-key-here")
    exit(1)

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

print("✅ Gemini API key loaded (FREE tier - 60 requests/minute!)")

# Example: Chat with Gemini
def ask_gemini(prompt, max_retries=3):
    """
    Send a prompt to Google Gemini and get a response (FREE!)
    """
    for attempt in range(max_retries):
        try:
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            response = requests.post(
                GEMINI_API_URL,
                json=payload,
                timeout=30,
                verify=False  # For corporate proxy
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text
            elif response.status_code == 429:
                return "⚠️ Rate limit reached. Wait a moment and try again."
            else:
                return f"Error: {response.status_code} - {response.text[:200]}"
                
        except Exception as e:
            if attempt == max_retries - 1:
                return f"Error ({type(e).__name__}): {str(e)}"
    
    return "Error: Max retries exceeded"

# Example: Web scraping with Gemini analysis
def scrape_and_analyze(url):
    """
    Scrape a webpage and use Gemini AI to analyze the content (FREE!)
    """
    try:
        # Fetch the webpage
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        
        # Get the text content (limit to avoid token limits)
        content = response.text[:8000]  # Gemini has higher limits
        
        # Ask Gemini to analyze
        prompt = f"Analyze this webpage content and provide a brief summary:\n\n{content}"
        analysis = ask_gemini(prompt)
        
        return analysis
    except Exception as e:
        return f"Error scraping/analyzing: {str(e)}"

# Test API connection
def test_api_connection():
    """
    Test if the Gemini API is accessible
    """
    print("\n🔍 Testing Gemini API connection...")
    try:
        response = ask_gemini("Say 'Connection successful!' in 3 words.")
        if "Error" not in response:
            print("✅ Gemini API connection successful!")
            return True
        else:
            print(f"❌ API test failed: {response}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {type(e).__name__}: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🆓 FREE AI Web Scraping with Google Gemini")
    print("="*60)
    
    # Test API connection first
    if test_api_connection():
        # Test Gemini
        print("\n📝 Testing Gemini AI query...")
        response = ask_gemini("Explain web scraping in one simple sentence.")
        print("\n--- Gemini Response ---")
        print(response)
        
        # Test web scraping
        print("\n🌐 Testing web scraping + AI analysis...")
        url = "https://example.com"
        analysis = scrape_and_analyze(url)
        print("\n--- Website Analysis ---")
        print(analysis)
        
        print("\n" + "="*60)
        print("✅ All tests complete!")
        print("💡 Gemini Free Tier: 60 requests/minute, 1,500 requests/day")
        print("="*60)
    else:
        print("\n⚠️ Please set up your Gemini API key first.")


