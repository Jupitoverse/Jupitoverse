"""
Web scraping with ChatGPT - Version with SSL verification disabled
⚠️ Use this version if you're behind a corporate proxy with SSL inspection
"""
import os
import requests
import warnings
from openai import OpenAI
from dotenv import load_dotenv

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Load environment variables
load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY not found! Please create a .env file with your API key.")

# Initialize OpenAI client with SSL verification disabled
# ⚠️ This is less secure but necessary in some corporate environments
import httpx
http_client = httpx.Client(verify=False)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    http_client=http_client
)

print("✅ OpenAI API key loaded (SSL verification disabled for corporate proxy)")

# Example: Chat completion
def ask_chatgpt(prompt, model="gpt-3.5-turbo"):
    """
    Send a prompt to ChatGPT and get a response
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            timeout=30.0
        )
        return response.choices[0].message.content
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        return f"Error ({error_type}): {error_msg}"

# Example: Web scraping with ChatGPT analysis
def scrape_and_analyze(url):
    """
    Scrape a webpage and use ChatGPT to analyze the content
    """
    try:
        # Fetch the webpage (with SSL verification disabled)
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        
        # Get the text content (you can use BeautifulSoup for better parsing)
        content = response.text[:4000]  # Limit content to avoid token limits
        
        # Ask ChatGPT to analyze
        prompt = f"Analyze this webpage content and provide a brief summary:\n\n{content}"
        analysis = ask_chatgpt(prompt)
        
        return analysis
    except Exception as e:
        return f"Error scraping/analyzing: {str(e)}"

# Test API connection
def test_api_connection():
    """
    Test if the OpenAI API is accessible
    """
    print("\n🔍 Testing API connection...")
    try:
        # Try a simple API call
        response = client.models.list()
        print("✅ API connection successful!")
        return True
    except Exception as e:
        print(f"❌ API connection failed: {type(e).__name__}: {str(e)}")
        print("\n💡 Possible solutions:")
        print("   1. Check your internet connection")
        print("   2. Verify your API key is valid at: https://platform.openai.com/api-keys")
        print("   3. Contact your IT department about proxy settings")
        return False

# Example usage
if __name__ == "__main__":
    # Test API connection first
    if test_api_connection():
        # Test the ChatGPT function
        print("\n📝 Testing ChatGPT query...")
        response = ask_chatgpt("Say 'Hello! I'm working!' in one short sentence.")
        print("\n--- ChatGPT Response ---")
        print(response)
        
        # Example: Scrape and analyze a webpage
        print("\n🌐 Testing web scraping...")
        url = "https://example.com"
        analysis = scrape_and_analyze(url)
        print("\n--- Website Analysis ---")
        print(analysis)
    else:
        print("\n⚠️ Skipping tests due to API connection issues.")


