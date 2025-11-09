import streamlit as st
import pdf2image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_chroma import Chroma
import base64
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools import tool
import os
import re
from datetime import datetime
import tempfile
import shutil

# Page config
st.set_page_config(
    page_title="Exam Grading System",
    page_icon="📝",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .score-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #3498db;
    }
    .grade-badge {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .grade-a { background-color: #d4edda; color: #155724; }
    .grade-b { background-color: #d1ecf1; color: #0c5460; }
    .grade-c { background-color: #fff3cd; color: #856404; }
    .grade-d { background-color: #f8d7da; color: #721c24; }
    .grade-f { background-color: #f5c6cb; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'grading_complete' not in st.session_state:
    st.session_state.grading_complete = False
if 'results' not in st.session_state:
    st.session_state.results = None

# API Key configuration
os.environ["GEMINI_API_KEY"] = "AIzaSyBq1Oce_OooZduoZXHz3-ze434hpRGcE3w"
os.environ["GOOGLE_API_KEY"] = "AIzaSyBq1Oce_OooZduoZXHz3-ze434hpRGcE3w"

GRADING_SEED = 42

@st.cache_resource
def initialize_vector_store():
    """Initialize the vector store with marking scheme."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vector_store = Chroma(
        collection_name="exam_sheet_evaluator",
        embedding_function=embeddings,
        persist_directory="./memory_vector_database",
    )
    
    marking_scheme_file_path = "./example_data/Physics-MS.pdf"
    
    # Check if already loaded
    existing_docs = vector_store.get()
    if not existing_docs['ids']:
        loader = PyMuPDF4LLMLoader(marking_scheme_file_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        
        all_splits = text_splitter.split_documents(docs)
        vector_store.add_documents(documents=all_splits)
    
    return vector_store

def create_retrieve_tool(vector_store):
    """Create the retrieve context tool."""
    @tool(description="Retrieve relevant sections from the marking scheme based on a query")
    def retrieve_context(query: str) -> str:
        """Retrieve context from the marking scheme."""
        retrieved_docs = vector_store.similarity_search(query, k=3)
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )
        return serialized
    
    return retrieve_context

def create_section_prompt(section_name, section_description):
    """Create a standardized prompt for grading a specific section."""
    return f'''
You are a professor at Delhi Technological University grading physics exam sheets.

SECTION TO GRADE: {section_name}
{section_description}

GRADING RUBRIC (follow strictly):
- Full marks: Answer is completely correct with proper methodology
- 75% marks: Answer is mostly correct with minor errors
- 50% marks: Answer shows understanding but has significant errors
- 25% marks: Answer shows some attempt but major conceptual errors
- 0 marks: No answer, completely wrong, or irrelevant

INSTRUCTIONS:
1. Analyze ONLY the {section_name} in the provided exam sheet images
2. Use the retrieve_context tool to fetch the marking scheme for this section
3. Compare each answer against the marking scheme
4. Award marks based on the rubric above
5. Ignore rough work - only grade final answers
6. Be consistent in your grading

OUTPUT FORMAT (strictly follow):
For EVERY question in this section, use this EXACT format:

Question X: [Marks Awarded]/[Total Marks Available]
────────────────────────────────────────────────────────────────────────────────
Student's Answer:
[Brief summary of what the student wrote]

Expected Answer (from Marking Scheme):
[Key points from the marking scheme]

Evaluation:
✓ Correct: [What was correct]
✗ Missing/Incorrect: [What was wrong or missing]

Marks Breakdown:
[Explain how marks were distributed based on the rubric]
────────────────────────────────────────────────────────────────────────────────
'''

def process_pdf(uploaded_file, progress_bar, status_text):
    """Process the uploaded PDF and grade it."""
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    
    try:
        # Initialize vector store and tools
        status_text.text("Loading marking scheme...")
        vector_store = initialize_vector_store()
        retrieve_context = create_retrieve_tool(vector_store)
        
        # Initialize LLM - no token limit to allow complete grading
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.0,
            max_tokens=None,  # No limit - let it generate complete response
            timeout=None,
            max_retries=2,
            seed=GRADING_SEED,
        )
        llm = llm.bind_tools([retrieve_context])
        
        # Convert PDF to images
        status_text.text("Converting PDF to images...")
        images = pdf2image.convert_from_path(tmp_path)
        progress_bar.progress(10)
        
        # Encode images
        status_text.text(f"Processing {len(images)} pages...")
        encoded_images = []
        for i, img in enumerate(images):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_img:
                img.save(tmp_img.name, 'JPEG')
                with open(tmp_img.name, 'rb') as f:
                    encoded = base64.b64encode(f.read()).decode('utf-8')
                    encoded_images.append(encoded)
                os.unlink(tmp_img.name)
        
        progress_bar.progress(20)
        
        # Define sections (EXACT copy from working agentmake.py)
        sections = [
            {
                "name": "Section A - Multiple Choice Questions",
                "description": "Grade all MCQ questions (typically Questions 1-16). Each correct answer gets full marks, incorrect gets 0.",
                "page_range": range(0, min(10, len(encoded_images)))
            },
            {
                "name": "Section B - Short Answer Questions",
                "description": "Grade all short answer questions. Apply the grading rubric based on completeness and accuracy.",
                "page_range": range(10, min(20, len(encoded_images)))
            },
            {
                "name": "Section C - Long Answer Questions",
                "description": "Grade all long answer questions. Check for methodology, steps, and final answers.",
                "page_range": range(20, min(30, len(encoded_images)))
            },
            {
                "name": "Section D - Numerical Problems",
                "description": "Grade all numerical problems. Check calculations, units, and final answers.",
                "page_range": range(30, len(encoded_images))
            }
        ]
        
        all_section_results = []
        progress_step = 60 / len(sections)
        
        # Process each section separately (EXACT copy from working CLI version)
        for section_idx, section in enumerate(sections):
            status_text.text(f"Grading {section['name']}...")
            
            # Create section-specific prompt
            section_prompt = create_section_prompt(section['name'], section['description'])
            
            # Prepare message with only relevant pages
            message_content = [{"type": "text", "text": section_prompt}]
            
            # Add images for this section
            for page_idx in section['page_range']:
                if page_idx < len(encoded_images):
                    message_content.append({
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{encoded_images[page_idx]}"
                    })
            
            message_local = HumanMessage(content=message_content)
            messages = [message_local]
            
            # Invoke LLM for this section
            result_local = llm.invoke(messages)
            
            # Handle tool calls
            max_iterations = 10
            iteration = 0
            while result_local.tool_calls and iteration < max_iterations:
                messages.append(result_local)
                
                for tool_call in result_local.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    tool_id = tool_call["id"]
                    
                    if tool_name == "retrieve_context":
                        tool_result = retrieve_context.invoke(tool_args)
                    else:
                        tool_result = f"Unknown tool: {tool_name}"
                    
                    tool_message = ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_id,
                    )
                    messages.append(tool_message)
                
                result_local = llm.invoke(messages)
                iteration += 1
            
            # Extract content
            if isinstance(result_local.content, list):
                section_content = "\n".join([item.get('text', str(item)) if isinstance(item, dict) else str(item) for item in result_local.content])
            else:
                section_content = str(result_local.content)
            
            all_section_results.append({
                "name": section['name'],
                "content": section_content
            })
            
            progress_bar.progress(20 + int((section_idx + 1) * progress_step))
        
        # Combine all section results
        combined_content = "\n\n".join([
            f"{'='*100}\n{section['name']}\n{'='*100}\n{section['content']}"
            for section in all_section_results
        ])
        
        # Parse results
        status_text.text("Calculating final scores...")
        combined_content = "\n\n".join([
            f"{section['name']}\n{'='*80}\n{section['content']}"
            for section in all_section_results
        ])
        
        marks_pattern = r'Question\s+\d+:\s*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)'
        matches = re.findall(marks_pattern, combined_content)
        
        # Check if grading is complete
        num_questions_graded = len(matches)
        
        total_obtained = 0
        total_possible = 0
        question_scores = []
        
        for obtained, possible in matches:
            obtained_float = float(obtained)
            possible_float = float(possible)
            total_obtained += obtained_float
            total_possible += possible_float
            question_scores.append((obtained_float, possible_float))
        
        # Calculate grade
        if total_possible > 0:
            percentage = (total_obtained / total_possible) * 100
            if percentage >= 90:
                grade = "A+"
            elif percentage >= 80:
                grade = "A"
            elif percentage >= 70:
                grade = "B+"
            elif percentage >= 60:
                grade = "B"
            elif percentage >= 50:
                grade = "C"
            elif percentage >= 40:
                grade = "D"
            else:
                grade = "F"
        else:
            percentage = 0
            grade = "N/A"
        
        progress_bar.progress(100)
        status_text.text("Grading complete!")
        
        return {
            "sections": all_section_results,
            "total_obtained": total_obtained,
            "total_possible": total_possible,
            "percentage": percentage,
            "grade": grade,
            "question_scores": question_scores,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    finally:
        # Cleanup
        os.unlink(tmp_path)

# Main UI
st.markdown('<div class="main-header">📝 Exam Grading System</div>', unsafe_allow_html=True)
st.markdown("### Upload your exam answer sheet PDF to get automated grading")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This system automatically grades physics exam sheets using AI.
    
    **Features:**
    - Automated grading with marking scheme
    - Question-wise evaluation
    - Detailed feedback
    - Consistent results (Temperature=0, Seed=42)
    """)
    
    st.header("📋 Instructions")
    st.write("""
    1. Upload your exam PDF
    2. Click 'Grade Exam'
    3. Wait for processing
    4. View detailed results
    """)

# Main content
uploaded_file = st.file_uploader("Choose exam PDF file", type=['pdf'])

if uploaded_file is not None:
    st.success(f"✓ File uploaded: {uploaded_file.name}")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🚀 Grade Exam", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner("Processing..."):
                results = process_pdf(uploaded_file, progress_bar, status_text)
                st.session_state.results = results
                st.session_state.grading_complete = True
            
            st.balloons()

# Display results
if st.session_state.grading_complete and st.session_state.results:
    results = st.session_state.results
    
    st.markdown("---")
    st.markdown("## 📊 Grading Results")
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Score", f"{results['total_obtained']:.1f}/{results['total_possible']:.1f}")
    
    with col2:
        st.metric("Percentage", f"{results['percentage']:.2f}%")
    
    with col3:
        grade_class = f"grade-{results['grade'][0].lower()}"
        st.markdown(f'<div class="grade-badge {grade_class}">{results["grade"]}</div>', unsafe_allow_html=True)
    
    with col4:
        st.metric("Questions Graded", len(results['question_scores']))
    
    # Question-wise scores
    st.markdown("### 📈 Question-wise Scores")
    
    # Create a bar chart
    import pandas as pd
    df = pd.DataFrame(results['question_scores'], columns=['Obtained', 'Total'])
    df['Question'] = [f"Q{i+1}" for i in range(len(df))]
    df['Percentage'] = (df['Obtained'] / df['Total'] * 100).round(1)
    
    st.bar_chart(df.set_index('Question')['Percentage'])
    
    # Detailed table
    with st.expander("📋 View Detailed Score Table"):
        st.dataframe(df, use_container_width=True)
    
    # Section-wise results
    st.markdown("### 📝 Detailed Evaluation")
    
    for section in results['sections']:
        with st.expander(f"📂 {section['name']}", expanded=False):
            st.markdown(section['content'])
    
    # Download button
    st.markdown("---")
    full_report = f"""
EXAM GRADING REPORT
{'='*100}
Date: {results['timestamp']}
Exam: Physics

SUMMARY:
Total Score: {results['total_obtained']:.1f}/{results['total_possible']:.1f}
Percentage: {results['percentage']:.2f}%
Grade: {results['grade']}
Questions Graded: {len(results['question_scores'])}

QUESTION-WISE SCORES:
"""
    for idx, (obtained, possible) in enumerate(results['question_scores'], 1):
        full_report += f"Question {idx}: {obtained:.1f}/{possible:.1f}\n"
    
    full_report += f"\n{'='*100}\nDETAILED EVALUATION:\n{'='*100}\n\n"
    
    for section in results['sections']:
        full_report += f"\n{section['name']}\n{'='*80}\n{section['content']}\n\n"
    
    st.download_button(
        label="📥 Download Full Report",
        data=full_report,
        file_name=f"grading_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>Powered by Google Gemini AI | Delhi Technological University</p>
</div>
""", unsafe_allow_html=True)
