# Quick Start Guide - RAG Pipeline

## 🚀 Get Started in 3 Steps

### Step 1: Download Model (One-Time Setup)

**Windows:**
```bash
cd "semantic-nlpupdate\DTU MOD\rag"
DOWNLOAD_MODEL.bat
```

**Linux/Mac:**
```bash
cd "semantic-nlpupdate/DTU MOD/rag"
pip install -r requirements.txt
python download_deepseek_model.py
```

⏱️ **Time**: 10-30 minutes (one-time only)  
💾 **Space**: ~15GB required  
🌐 **Internet**: Required for download only

---

### Step 2: Prepare Your Input

1. Open your Excel file with service requests
2. Ensure it has these columns:
   - SR ID (or Call ID)
   - Priority
   - Description
   - Semantic Workaround
3. Save it in: `DTU MOD/input/`

**Example:**

| SR ID | Priority | Description | Semantic Workaround |
|-------|----------|-------------|---------------------|
| SR001 | P1 | Database connection error | Restart service... |
| SR002 | P2 | Java NullPointerException | Check configuration... |

---

### Step 3: Run the Pipeline

**Windows:**
```bash
RUN_RAG_PIPELINE.bat
```

**Linux/Mac:**
```bash
python rag_pipeline.py
```

✅ **Output**: `DTU MOD/llm output/<filename>_analysis_<timestamp>.xlsx`

---

## 📊 What You'll Get

Your output Excel will have:

✅ **Java Failure Detection** - Automatic Java backend error identification  
✅ **Optimal Assignment** - Skills-based team member assignment  
✅ **AI Workarounds** - Enhanced solutions from DeepSeek LLM  
✅ **Troubleshooting Steps** - Step-by-step resolution guide  
✅ **Complete Analysis** - All original data preserved

---

## 💡 Pro Tips

### For Best Results

1. **Run extract_semantic_workarounds.py first** to generate semantic workarounds column
2. **Use GPU** if available for 5x faster processing
3. **Process in batches** of 50-100 SRs for optimal performance
4. **Keep databases updated** - Refresh javaMapping.db and people_skills.db regularly

### Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| Model not found | Run `DOWNLOAD_MODEL.bat` |
| Out of memory | Close other apps, use CPU mode |
| No Excel found | Place file in `DTU MOD/input/` |
| Slow processing | Enable GPU, reduce max_tokens |

---

## 🎯 Example Workflow

```
1. extract_semantic_workarounds.py
   └─→ Generates: file_with_Semantic_Workarounds.xlsx

2. Move to: DTU MOD/input/

3. RUN_RAG_PIPELINE.bat
   └─→ Generates: file_analysis_20241114_153045.xlsx

4. Review in: DTU MOD/llm output/
```

---

## ⚡ Performance

| SRs | GPU Time | CPU Time |
|-----|----------|----------|
| 10 | 1-2 min | 5-10 min |
| 50 | 5-10 min | 25-50 min |
| 100 | 10-20 min | 50-100 min |

---

## 🔒 Offline Mode

After initial download:
- ✅ No internet required
- ✅ Corporate firewall friendly
- ✅ 100% local processing
- ✅ Data privacy protected

---

## 📞 Need Help?

Check the full documentation: `README.md`

**Common Issues:**
- Model download fails → Check internet/firewall
- GPU out of memory → Use CPU mode
- Wrong columns → Check Excel format
- Slow processing → Use GPU, reduce SRs

---

**Ready to analyze? Run `RUN_RAG_PIPELINE.bat` now!** 🚀

