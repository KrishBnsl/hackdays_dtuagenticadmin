# 📦 Installation Guide

## Super Simple Installation

### One Command Install
```bash
pip install -r requirements.txt
```

That's it! This installs everything you need.

### Or Use the Install Script
```bash
./install.sh
```

This will:
- Check your Python version
- Install all dependencies
- Verify installation

## Verify Installation

Run the test script:
```bash
python test_ui.py
```

Expected output:
```
✓ streamlit
✓ pdf2image
✓ langchain
✓ langchain_google_genai
✓ langchain_chroma
✓ PIL

✓ poppler-utils installed
✓ app.py - Main application file
✓ requirements.txt - Dependencies file
✓ ./example_data/Physics-MS.pdf - Marking scheme PDF
✓ API key found in environment

✅ All checks passed! You're ready to run the application.
```

## Run the Application

### Option 1: Use the Launcher (Recommended)
```bash
./run_ui.sh
```

This automatically:
- Sets up environment variables
- Checks dependencies
- Starts the application

### Option 2: Direct Command
```bash
export KMP_DUPLICATE_LIB_OK=TRUE  # Fix for macOS OpenMP issue
streamlit run app.py
```

## Troubleshooting

### "Module not found" errors
```bash
# Install all dependencies
pip install -r requirements.txt

# Or for conda
conda install -c conda-forge streamlit
```

### OpenMP Error on macOS
If you see "Initializing libomp.dylib" error:
```bash
export KMP_DUPLICATE_LIB_OK=TRUE
streamlit run app.py
```

Or just use `./run_ui.sh` which handles this automatically.

### PDF Conversion Fails
Install poppler:
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

## What Gets Installed

When you run `pip install -r requirements.txt`:

- **streamlit** - Web UI framework
- **pdf2image** - PDF to image conversion
- **langchain** - LLM framework
- **langchain-google-genai** - Google Gemini integration
- **langchain-chroma** - Vector database
- **langchain-pymupdf4llm** - PDF loading
- **PyMuPDF** - PDF processing
- **chromadb** - Vector storage
- **Pillow** - Image processing
- **pandas** - Data handling

## System Requirements

- **Python**: 3.8+ (you have 3.13.5 ✓)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 500MB for dependencies
- **Internet**: Required for API calls

## Next Steps

After installation:
1. Run `python test_ui.py` to verify
2. Run `./run_ui.sh` to start
3. Open browser to `http://localhost:8501`
4. Upload a PDF and test!

## Quick Reference

```bash
# Install
conda install -c conda-forge streamlit

# Verify
python test_ui.py

# Run
./run_ui.sh

# Access
http://localhost:8501
```

That's it! You're ready to grade exams! 🎉
