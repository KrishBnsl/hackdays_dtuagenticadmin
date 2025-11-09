# 🚀 Quick Setup Guide

## Step 1: Install Streamlit

```bash
pip install streamlit
```

Or install all dependencies at once:

```bash
pip install -r requirements.txt
```

## Step 2: Verify Setup

```bash
python test_ui.py
```

This will check if everything is properly configured.

## Step 3: Run the Application

**Option A - Using the launcher script:**
```bash
./run_ui.sh
```

**Option B - Direct command:**
```bash
streamlit run app.py
```

## Step 4: Use the Application

1. Your browser should open automatically to `http://localhost:8501`
2. Upload your exam PDF file
3. Click "Grade Exam"
4. Wait for processing (may take 2-5 minutes)
5. View results and download report

## 📋 What You'll See

### Main Interface
- **Upload Section**: Drag and drop your exam PDF
- **Grade Button**: Start the grading process
- **Progress Bar**: Real-time processing status

### Results Dashboard
- **Summary Cards**: Total score, percentage, grade, questions graded
- **Bar Chart**: Visual representation of question-wise scores
- **Detailed Table**: Expandable score breakdown
- **Section Results**: Detailed evaluation for each section
- **Download Button**: Export full report as text file

## 🎨 Features

### Visual Elements
- Clean, modern interface
- Color-coded grades (A+ = Green, F = Red)
- Interactive charts
- Expandable sections for detailed view

### Grading Features
- Section-by-section processing (MCQs, Short Answers, Long Answers, Numerical)
- AI-powered evaluation with marking scheme
- Consistent results (Temperature=0, Fixed Seed=42)
- Question-wise feedback
- Automatic score calculation

### Export Options
- Download full grading report
- Includes timestamp, scores, and detailed evaluation
- Plain text format for easy sharing

## ⚙️ Configuration

### Adjust Section Page Ranges
Edit `app.py` around line 200:

```python
sections = [
    {
        "name": "Section A - Multiple Choice Questions",
        "page_range": range(0, 10)  # Adjust these numbers
    },
    # ... other sections
]
```

### Change Grading Seed
Edit `app.py` line 54:

```python
GRADING_SEED = 42  # Change to any number
```

### Update API Key
Edit `app.py` lines 51-52 with your own API key.

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### PDF conversion fails
Make sure poppler is installed:
- macOS: `brew install poppler`
- Ubuntu: `sudo apt-get install poppler-utils`

### Application won't start
Check if port 8501 is already in use:
```bash
lsof -i :8501
```

### Slow processing
- Normal for large PDFs (30+ pages)
- First run initializes vector database (slower)
- Subsequent runs are faster

## 💡 Tips

1. **Clear and Readable PDFs**: Better image quality = better grading
2. **Proper Marking Scheme**: Ensure marking scheme PDF is well-formatted
3. **Consistent Exam Format**: Works best with standardized exam layouts
4. **Internet Connection**: Required for API calls to Gemini

## 📊 Expected Processing Times

- Small exam (10 pages): ~1-2 minutes
- Medium exam (20 pages): ~3-5 minutes
- Large exam (40 pages): ~5-10 minutes

## 🎯 Next Steps

After successful setup:
1. Test with a sample exam PDF
2. Verify grading accuracy
3. Adjust section ranges if needed
4. Customize grading rubric in prompts
5. Share with your team!

---

**Need Help?** Run `python test_ui.py` to diagnose issues.
