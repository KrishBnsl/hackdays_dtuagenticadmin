#!/bin/bash

echo "📦 Installing Exam Grading System Dependencies..."
echo ""

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install dependencies
echo ""
echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "To verify installation, run:"
    echo "  python test_ui.py"
    echo ""
    echo "To start the application, run:"
    echo "  ./run_ui.sh"
else
    echo ""
    echo "❌ Installation failed!"
    echo "Please check the error messages above."
    exit 1
fi
