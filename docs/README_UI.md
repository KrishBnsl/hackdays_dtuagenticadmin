# Exam Grading System - Web UI

A web-based interface for automated exam grading using AI.

## Features

- 📤 **Easy PDF Upload** - Simply drag and drop your exam PDF
- 🤖 **AI-Powered Grading** - Uses Google Gemini for intelligent evaluation
- 📊 **Visual Results** - Interactive charts and detailed breakdowns
- 📝 **Question-wise Feedback** - See evaluation for each question
- 💾 **Download Reports** - Export full grading reports
- 🎯 **Consistent Results** - Deterministic grading (Temperature=0, Fixed Seed)

## Installation

1. Install system dependencies (for PDF processing):

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the web application:
```bash
streamlit run app.py
```

2. Open your browser (should open automatically) to `http://localhost:8501`

3. Upload your exam PDF file

4. Click "Grade Exam" and wait for processing

5. View results:
   - Overall score and grade
   - Question-wise breakdown
   - Detailed evaluation for each section
   - Download full report

## How It Works

1. **PDF Processing** - Converts exam pages to images
2. **Section-wise Grading** - Processes exam in sections (MCQs, Short Answers, Long Answers, Numerical)
3. **AI Evaluation** - Uses Gemini AI with marking scheme retrieval
4. **Result Compilation** - Calculates scores using Python for accuracy
5. **Visual Display** - Shows results in an interactive dashboard

## Configuration

- **Marking Scheme**: Place your marking scheme PDF at `./example_data/Physics-MS.pdf`
- **API Key**: Update the API key in `app.py` (lines 51-52)
- **Grading Seed**: Change `GRADING_SEED` for different random behavior (default: 42)
- **Section Ranges**: Adjust page ranges in the `sections` list based on your exam structure

## Tips for Best Results

- Ensure exam PDF is clear and readable
- Marking scheme should be properly formatted
- First run may take longer (initializing vector database)
- Subsequent runs are faster (cached marking scheme)

## Troubleshooting

**PDF conversion fails:**
- Make sure poppler is installed
- Check PDF is not corrupted

**Grading takes too long:**
- Large PDFs (>40 pages) may take 5-10 minutes
- Check your internet connection (API calls)

**Inconsistent results:**
- Temperature is set to 0 for consistency
- Seed is fixed at 42
- If still inconsistent, check marking scheme quality

## Support

For issues or questions, check the console output for detailed error messages.
