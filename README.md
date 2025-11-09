# 📝 Exam Grading System

AI-powered automated exam grading system with web interface for physics exams.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install poppler (for PDF processing)
brew install poppler  # macOS
# sudo apt-get install poppler-utils  # Ubuntu

# 3. Run the web application
./run_ui.sh

# 4. Open browser to http://localhost:8501
```

## ✨ Features

- **Web Interface** - Upload PDFs via drag-and-drop
- **AI-Powered Grading** - Uses Google Gemini for intelligent evaluation
- **Marking Scheme Integration** - Retrieves relevant sections automatically
- **Question-wise Feedback** - Detailed evaluation for each question
- **Visual Dashboard** - Interactive charts and score breakdowns
- **Downloadable Reports** - Export complete grading reports
- **Consistent Results** - Deterministic grading (Temperature=0, Fixed Seed=42)

## 📁 Project Structure

```
exam-grading-system/
├── app.py                      # Web UI (Streamlit)
├── agentmake.py               # CLI version
├── requirements.txt           # Python dependencies
├── run_ui.sh                  # Web app launcher
├── install.sh                 # Dependency installer
├── example_data/              # Marking schemes
│   └── Physics-MS.pdf
├── temp_images/               # Temporary files (auto-generated)
├── memory_vector_database/    # Vector DB (auto-generated)
└── docs/                      # Additional documentation
```

## 🎯 Usage

### Web Interface (Recommended)

1. **Start the application:**
   ```bash
   ./run_ui.sh
   ```

2. **Upload exam PDF** - Drag and drop or click to browse

3. **Click "Grade Exam"** - Processing takes 2-5 minutes depending on exam size

4. **View results:**
   - Summary cards (total score, percentage, grade)
   - Question-wise bar chart
   - Detailed evaluation for each section
   - Download full report

### Command Line Interface

```bash
python agentmake.py
```

Edit the file to change the input PDF path (default: `./Physics.pdf`)

## ⚙️ Configuration

### Marking Scheme
Place your marking scheme PDF at:
```
./example_data/Physics-MS.pdf
```

### API Key
Update the Google API key in `app.py` or `agentmake.py`:
```python
os.environ["GOOGLE_API_KEY"] = "your-api-key-here"
```

### Grading Parameters
Adjust in the code:
- **Temperature**: `0.0` (for consistency)
- **Seed**: `42` (for reproducibility)
- **Section Page Ranges**: Modify the `sections` list to match your exam structure

## 📊 How It Works

1. **PDF Processing** - Converts exam pages to images
2. **Section-wise Grading** - Processes in sections:
   - Section A: Multiple Choice Questions (pages 0-10)
   - Section B: Short Answer Questions (pages 10-20)
   - Section C: Long Answer Questions (pages 20-30)
   - Section D: Numerical Problems (pages 30+)
3. **AI Evaluation** - Uses Google Gemini with marking scheme retrieval
4. **Score Calculation** - Python ensures accurate totals
5. **Result Display** - Interactive dashboard with detailed feedback

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- Poppler (for PDF processing)

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or use the install script:
```bash
./install.sh
```

### Install Poppler

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**Windows:**
Download from: http://blog.alivate.com.au/poppler-windows/

## 🐛 Troubleshooting

### Module not found errors
```bash
pip install -r requirements.txt
```

### PDF conversion fails
Make sure poppler is installed:
```bash
# macOS
brew install poppler

# Ubuntu
sudo apt-get install poppler-utils
```

### OpenMP error (macOS)
The launcher script handles this automatically. If running manually:
```bash
export KMP_DUPLICATE_LIB_OK=TRUE
streamlit run app.py
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

## 📦 Dependencies

Main packages:
- `streamlit` - Web interface
- `langchain` - LLM framework
- `langchain-google-genai` - Google Gemini integration
- `langchain-chroma` - Vector database
- `pdf2image` - PDF processing
- `chromadb` - Vector storage

See `requirements.txt` for complete list with versions.

## 🎓 Grading Rubric

The system uses the following rubric:
- **Full marks**: Completely correct with proper methodology
- **75%**: Mostly correct with minor errors
- **50%**: Shows understanding but significant errors
- **25%**: Some attempt but major conceptual errors
- **0%**: No answer, completely wrong, or irrelevant

## 📈 Performance

- **Small exam (10 pages)**: 1-2 minutes
- **Medium exam (20 pages)**: 3-5 minutes
- **Large exam (40 pages)**: 5-10 minutes

First run is slower as it initializes the vector database. Subsequent runs are faster.

## 🔐 Security Notes

- API keys are currently hardcoded (for demo purposes)
- For production: Use environment variables
- Don't commit API keys to version control
- Consider adding user authentication for web interface

## 📚 Additional Documentation

See the `docs/` folder for:
- Detailed installation guides
- UI feature descriptions
- Complete documentation
- Visual guides

## 📝 License

See [LICENSE](LICENSE) file for details.

**Technologies:**
- [Streamlit](https://streamlit.io/) - Web UI framework
- [LangChain](https://langchain.com/) - LLM orchestration
- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI model
- [ChromaDB](https://www.trychroma.com/) - Vector database

