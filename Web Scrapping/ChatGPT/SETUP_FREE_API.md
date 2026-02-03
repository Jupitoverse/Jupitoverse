# 🆓 FREE AI API Setup Guide

Your OpenAI API requires billing, but there are **FREE alternatives** with generous limits!

## 🌟 Best FREE Option: Google Gemini

Google's Gemini API is **completely FREE** with generous limits:
- ✅ **60 requests per minute**
- ✅ **1,500 requests per day**
- ✅ **No credit card required**
- ✅ **Same capabilities as ChatGPT**

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Get FREE Gemini API Key

1. **Go to Google AI Studio:**
   https://makersuite.google.com/app/apikey

2. **Click "Create API Key"**
   - Sign in with your Google account
   - Click "Create API key in new project"
   - Copy the key

3. **Add to your `.env` file:**
   ```bash
   GEMINI_API_KEY=your-key-here
   ```

### Step 2: Run the FREE Version

```bash
python v2_gemini_free.py
```

That's it! 🎉

---

## 📊 Comparison: OpenAI vs Gemini (Free)

| Feature | OpenAI (Paid) | Gemini (FREE) |
|---------|---------------|---------------|
| **Cost** | $0.002/1K tokens | **FREE** |
| **Rate Limit** | Varies | 60/min, 1,500/day |
| **Setup** | Credit card required | **No billing needed** |
| **Quality** | Excellent | Excellent |
| **Web Scraping** | ✅ | ✅ |

---

## 📁 Project Files

### For FREE Gemini API:
- `v2_gemini_free.py` - Main script (FREE version)
- `.env` - Add your `GEMINI_API_KEY` here

### Original OpenAI Version:
- `v1.py` - OpenAI version (requires billing)
- Keep this if you want to use OpenAI later

---

## 🎯 What You Can Do (FREE)

With Gemini's free tier:
- ✅ **1,500 AI requests per day** - more than enough for development!
- ✅ Web scraping + AI analysis
- ✅ Chat/Q&A functionality
- ✅ Content summarization
- ✅ Data extraction

---

## 💡 Example Usage

```python
from v2_gemini_free import ask_gemini, scrape_and_analyze

# Simple AI query
response = ask_gemini("What is web scraping?")
print(response)

# Scrape and analyze a website
analysis = scrape_and_analyze("https://example.com")
print(analysis)
```

---

## 🔗 Useful Links

- **Get API Key:** https://makersuite.google.com/app/apikey
- **Gemini Docs:** https://ai.google.dev/docs
- **Free Tier Limits:** https://ai.google.dev/pricing

---

## ⚡ Other FREE Alternatives

### Option 2: Hugging Face (FREE)
- **API:** https://huggingface.co/inference-api
- **Limits:** 30K characters/request (free)
- **Setup:** Create account, get API token

### Option 3: Ollama (Local - Completely FREE)
- **Website:** https://ollama.ai
- **Runs on your computer** (no API key needed)
- **Models:** Llama 2, Mistral, etc.
- **Best for:** Unlimited usage, privacy

---

## 🎉 Recommendation

**Use Gemini (v2_gemini_free.py)** - Best balance of:
- ✅ FREE with generous limits
- ✅ Easy setup (5 minutes)
- ✅ Excellent quality
- ✅ No local installation needed

---

**Ready to start?** Just:
1. Get your FREE Gemini key: https://makersuite.google.com/app/apikey
2. Add to `.env`: `GEMINI_API_KEY=your-key`
3. Run: `python v2_gemini_free.py`

**No billing, no credit card, just code!** 🚀


