# 📝 Exam Grading System - Complete Guide

## 🚀 Quick Start (3 Commands)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
./run_ui.sh

# 3. Open browser to http://localhost:8501
```

That's it! 🎉

---

## 📋 What This Does

Automatically grades physics exam sheets using AI:
- Upload PDF → Get detailed grading
- Question-wise evaluation
- Consistent, reproducible results
- Beautiful web interface

---

## 🎯 Features

### For Students/Teachers
- ✅ Upload exam PDF via drag-and-drop
- ✅ Get instant grading results
- ✅ See question-wise scores
- ✅ Download detailed report
- ✅ Visual charts and breakdowns

### Technical Features
- ✅ AI-powered with Google Gemini
- ✅ Marking scheme integration
- ✅ Section-by-section processing
- ✅ Temperature=0, Seed=42 (consistent results)
- ✅ Python-calculated totals (accurate)
- ✅ Validation loop for quality

---

## 📦 Installation

### Method 1: One Command
```bash
pip install -r requirements.txt
```

### Method 2: Install Script
```bash
./install.sh
```

### Verify Installation
```bash
python test_ui.py
```

Expected output:
```
✓ streamlit
✓ pdf2image
✓ langchain
✓ All checks passed!
```

---

## 🎮 Usage

### Start the Application

**Option A: Use launcher (recommended)**
```bash
./run_ui.sh
```

**Option B: Direct command**
```bash
export KMP_DUPLICATE_LIB_OK=TRUE  # macOS only
streamlit run app.py
```

### Using the Web Interface

1. **Open browser** → `http://localhost:8501`
2. **Upload PDF** → Drag and drop your exam
3. **Click "Grade Exam"** → Wait 2-5 minutes
4. **View Results** → Interactive dashboard
5. **Download Report** → Save for records

---

## 📊 What You'll See

### Summary Dashboard
```
┌────────────────┬────────────────┬────────────────┬────────────────┐
│  Total Score   │  Percentage    │     Grade      │   Questions    │
│    85.5/100    │    85.50%      │       A        │   Graded: 25   │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

### Visual Charts
- Bar chart of question scores
- Color-coded grades (A+ to F)
- Interactive expandable sections

### Detailed Evaluation
For each question:
- Student's answer summary
- Expected answer from marking scheme
- What was correct/incorrect
- Marks breakdown with explanation

---

## 🔧 Configuration

### Adjust Section Page Ranges
Edit `app.py` around line 200:
```python
sections = [
    {
        "name": "Section A - Multiple Choice Questions",
        "page_range": range(0, 10)  # Change these numbers
    },
    # ... more sections
]
```

### Change Grading Seed
Edit `app.py` line 54:
```python
GRADING_SEED = 42  # Change for different behavior
```

### Update API Key
Edit `app.py` lines 51-52 with your Google API key.

---

## 📁 Project Structure

```
.
├── app.py                  # Main Streamlit web application
├── agentmake.py           # CLI version (original)
├── requirements.txt       # Python dependencies
├── install.sh            # Installation script
├── run_ui.sh             # Launcher script
├── test_ui.py            # Verification tool
├── QUICK_START.md        # Quick reference
├── INSTALL.md            # Detailed installation
├── UI_SUMMARY.md         # Feature overview
└── example_data/
    └── Physics-MS.pdf    # Marking scheme
```

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### OpenMP Error (macOS)
```bash
export KMP_DUPLICATE_LIB_OK=TRUE
streamlit run app.py
```
Or just use `./run_ui.sh` which handles this.

### PDF Conversion Fails
Install poppler:
```bash
# macOS
brew install poppler

# Ubuntu
sudo apt-get install poppler-utils
```

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Slow Processing
- Normal for large PDFs (30+ pages)
- First run is slower (initializes database)
- Subsequent runs are faster

---

## 📚 Documentation

- **QUICK_START.md** - 3-step quick start
- **INSTALL.md** - Detailed installation guide
- **UI_SUMMARY.md** - Complete feature list
- **UI_FEATURES.md** - Visual design guide
- **SETUP_GUIDE.md** - Configuration options
- **VISUAL_GUIDE.txt** - ASCII art preview

---

## 🎯 How It Works

1. **PDF Upload** → Converts to images
2. **Section Processing** → Breaks into MCQs, Short, Long, Numerical
3. **AI Grading** → Uses Gemini with marking scheme
4. **Score Calculation** → Python ensures accuracy
5. **Result Display** → Interactive dashboard

---

## ⚙️ System Requirements

- **Python**: 3.8+ (tested on 3.13.5)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 500MB for dependencies
- **Internet**: Required for API calls
- **Browser**: Modern browser (Chrome, Firefox, Safari)

---

## 📈 Performance

### Processing Times
- Small exam (10 pages): 1-2 minutes
- Medium exam (20 pages): 3-5 minutes
- Large exam (40 pages): 5-10 minutes

### Optimization
- First run: Slower (initializes vector DB)
- Subsequent runs: Faster (cached)
- Section-by-section: More consistent

---

## 🔐 Security Notes

- API key is hardcoded (for demo)
- For production: Use environment variables
- Don't commit API keys to git
- Consider adding authentication

---

## 🚀 Next Steps

### After Setup
1. Test with sample exam
2. Verify grading accuracy
3. Adjust section ranges
4. Customize grading rubric
5. Share with team

### Future Enhancements
- User authentication
- Multiple marking schemes
- Grading history
- Batch processing
- Excel/CSV export
- Admin dashboard

---

## 💡 Tips

1. **Clear PDFs** → Better results
2. **Proper Marking Scheme** → Essential for accuracy
3. **Consistent Format** → Works best with standardized exams
4. **First Run** → Takes longer, be patient
5. **Check Logs** → Console shows progress

---

## 🆘 Getting Help

### Run Diagnostics
```bash
python test_ui.py
```

### Check Logs
Look at terminal output for detailed error messages.

### Common Issues
- Import errors → Run `pip install -r requirements.txt`
- PDF errors → Install poppler
- Port errors → Use different port
- Slow processing → Normal for large files

---

## 📝 License & Credits

Built with:
- Streamlit (Web UI)
- LangChain (LLM Framework)
- Google Gemini (AI Model)
- ChromaDB (Vector Store)

---

## 🎉 You're Ready!

Run this now:
```bash
./run_ui.sh
```

Then open `http://localhost:8501` and start grading! 🚀
