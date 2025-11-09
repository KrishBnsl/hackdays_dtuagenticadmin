#!/bin/bash

echo "🚀 Starting Exam Grading System..."
echo ""

# Fix for OpenMP library conflict on macOS
export KMP_DUPLICATE_LIB_OK=TRUE

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit is not installed!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Check if poppler is installed (for PDF processing)
if ! command -v pdfinfo &> /dev/null
then
    echo "⚠️  Warning: poppler-utils not found!"
    echo "PDF processing may fail. Install with:"
    echo "  macOS: brew install poppler"
    echo "  Ubuntu: sudo apt-get install poppler-utils"
    echo ""
fi

# Check if marking scheme exists
if [ ! -f "./example_data/Physics-MS.pdf" ]; then
    echo "⚠️  Warning: Marking scheme not found at ./example_data/Physics-MS.pdf"
    echo "Please ensure the marking scheme PDF is in the correct location."
    echo ""
fi

# Create temp_images directory if it doesn't exist
mkdir -p temp_images

echo "✓ Starting web interface..."
echo "✓ Open your browser to http://localhost:8501"
echo ""

streamlit run app.py
