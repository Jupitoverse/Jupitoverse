# AI Web Scraping Project

A Python project for web scraping with AI analysis capabilities.

## 🆓 FREE Version Available!

**Don't want to pay for OpenAI?** Use the **FREE Google Gemini version**!
- See: `SETUP_FREE_API.md` for setup
- Run: `python v2_gemini_free.py`

## 🚀 Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key:**
   - A `.env` file has been created with your API key
   - **IMPORTANT:** Never commit the `.env` file to version control!
   - The `.gitignore` file is already configured to protect your secrets

3. **Set up OpenAI Billing:**
   - Go to: https://platform.openai.com/account/billing
   - Add a payment method and credits (minimum $5 recommended)
   - GPT-3.5-Turbo costs ~$0.002 per 1K tokens (very affordable!)

4. **Run the script:**
   ```bash
   python v1.py
   ```

## 📦 Dependencies

- `openai` - OpenAI API client
- `requests` - HTTP library for web scraping
- `python-dotenv` - Load environment variables from .env file
- `httpx` - HTTP client for OpenAI (supports SSL configuration)
- `beautifulsoup4` - HTML parsing (optional, for advanced scraping)
- `lxml` - XML/HTML parser (optional)
- `selenium` - Browser automation (optional, for dynamic content)

## 🔒 Security Notes

- ✅ API keys are stored in `.env` file (not in code)
- ✅ `.env` is added to `.gitignore`
- ✅ Never share your `.env` file or commit it to git
- ⚠️ SSL verification is disabled for corporate proxy compatibility
  - If you're NOT behind a corporate proxy, you can remove the `http_client` parameter from the OpenAI client initialization

## 📝 Usage Examples

### Basic ChatGPT Query
```python
response = ask_chatgpt("Your question here")
print(response)
```

### Scrape and Analyze a Webpage
```python
analysis = scrape_and_analyze("https://example.com")
print(analysis)
```

## ⚠️ Important Notes

1. **Security:** Your API key was previously exposed in the code. It has been moved to the `.env` file for security. Consider rotating your API key at: https://platform.openai.com/api-keys

2. **Billing:** Make sure to add billing to your OpenAI account at: https://platform.openai.com/account/billing

3. **Corporate Proxy:** If you're behind a corporate proxy/firewall with SSL inspection, the code has been configured to handle this automatically.

4. **Testing:** Run `python test_connection.py` for detailed diagnostics if you encounter connection issues.

