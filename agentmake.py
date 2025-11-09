import pdf2image
from langchain.agents import create_agent
from transformers import AutoModel, AutoTokenizer
import torch
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
import pprint
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma
import base64
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools import tool

os.environ["GEMINI_API_KEY"] = "insert api key"
os.environ["GOOGLE_API_KEY"] = "insert api key"

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store = Chroma(
    collection_name="exam_sheet_evaluator",
    embedding_function=embeddings,
    persist_directory="./memory_vector_database",  
)

marking_scheme_file_path = "./example_data/Physics-MS.pdf"
loader = PyMuPDF4LLMLoader(marking_scheme_file_path)
docs = loader.load()
#pprint.pp(docs[0].metadata)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  #(characters)
    chunk_overlap=200,  # (characters)
    add_start_index=True,  
)

all_splits = text_splitter.split_documents(docs)

# Only add documents if the collection is empty (avoid duplicates)
existing_docs = vector_store.get()
if not existing_docs['ids']:
    document_ids = vector_store.add_documents(documents=all_splits)
    print(f"Added {len(document_ids)} document chunks to vector store")
else:
    print(f"Vector store already contains {len(existing_docs['ids'])} documents, skipping indexing")

@tool(description="Retrieve relevant sections from the marking scheme based on a query")
def retrieve_context(query: str) -> str:
    """Retrieve context from the marking scheme."""
    retrieved_docs = vector_store.similarity_search(query, k=3)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized

# Fixed seed for reproducibility
GRADING_SEED = 42

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.0,  # Set to 0 for maximum determinism
    max_tokens=None,
    timeout=None,
    max_retries=2,
    seed=GRADING_SEED,  # Add seed for reproducible results
)

llm = llm.bind_tools([retrieve_context])

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

print("Converting student exam PDF to images...")
images = pdf2image.convert_from_path('./Physics.pdf')
print(f"Converted {len(images)} pages")

for i in range(len(images)):
    images[i].save(f'temp_images/page{i}.jpg', 'JPEG')

l = []
for i in range(len(images)):
    image_file_path = f"./temp_images/page{i}.jpg"
    with open(image_file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        l.append(encoded_image)

print(f"Encoded {len(l)} images for processing")

# Define sections to grade
sections = [
    {
        "name": "Section A - Multiple Choice Questions",
        "description": "Grade all MCQ questions (typically Questions 1-16). Each correct answer gets full marks, incorrect gets 0.",
        "page_range": range(0, min(10, len(l)))  # Adjust based on your exam structure
    },
    {
        "name": "Section B - Short Answer Questions", 
        "description": "Grade all short answer questions. Apply the grading rubric based on completeness and accuracy.",
        "page_range": range(10, min(20, len(l)))
    },
    {
        "name": "Section C - Long Answer Questions",
        "description": "Grade all long answer questions. Check for methodology, steps, and final answers.",
        "page_range": range(20, min(30, len(l)))
    },
    {
        "name": "Section D - Numerical Problems",
        "description": "Grade all numerical problems. Check calculations, units, and final answers.",
        "page_range": range(30, len(l))
    }
]

all_section_results = []

# Process each section separately for consistency
for section_idx, section in enumerate(sections):
    print(f"\n{'='*80}")
    print(f"Processing {section['name']}...")
    print(f"{'='*80}")
    
    # Create section-specific prompt
    section_prompt = create_section_prompt(section['name'], section['description'])
    
    # Prepare message with only relevant pages
    message_content = [{"type": "text", "text": section_prompt}]
    
    # Add images for this section
    for page_idx in section['page_range']:
        if page_idx < len(l):
            message_content.append({
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{l[page_idx]}"
            })
    
    message_local = HumanMessage(content=message_content)
    messages = [message_local]
    
    # Invoke LLM for this section
    result_local = llm.invoke(messages)
    
    # Handle tool calls
    max_iterations = 10  # Prevent infinite loops
    iteration = 0
    while result_local.tool_calls and iteration < max_iterations:
        print(f"  Tool call: {result_local.tool_calls[0]['name']} - {result_local.tool_calls[0]['args'].get('query', '')[:50]}...")
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
    
    print(f"✓ Completed {section['name']}")

# Combine all section results
combined_content = "\n\n".join([
    f"{'='*100}\n{section['name']}\n{'='*100}\n{section['content']}"
    for section in all_section_results
])

from datetime import datetime
import re

# Parse marks from all sections
marks_pattern = r'Question\s+\d+:\s*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)'
matches = re.findall(marks_pattern, combined_content)

total_obtained = 0
total_possible = 0
question_scores = []

for obtained, possible in matches:
    obtained_float = float(obtained)
    possible_float = float(possible)
    total_obtained += obtained_float
    total_possible += possible_float
    question_scores.append((obtained_float, possible_float))

# Calculate percentage and grade
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

# Validation: Run a second pass to verify consistency
print("\n" + "="*80)
print("Running validation pass...")
print("="*80)

# Re-run grading on a sample section to check consistency
validation_section = sections[0]  # Validate Section A
validation_prompt = create_section_prompt(validation_section['name'], validation_section['description'])
validation_message = [{"type": "text", "text": validation_prompt}]

for page_idx in validation_section['page_range']:
    if page_idx < len(l):
        validation_message.append({
            "type": "image_url",
            "image_url": f"data:image/jpeg;base64,{l[page_idx]}"
        })

validation_result = llm.invoke([HumanMessage(content=validation_message)])

# Handle tool calls for validation
iteration = 0
while validation_result.tool_calls and iteration < 10:
    validation_messages = [HumanMessage(content=validation_message), validation_result]
    for tool_call in validation_result.tool_calls:
        if tool_call["name"] == "retrieve_context":
            tool_result = retrieve_context.invoke(tool_call["args"])
            validation_messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))
    validation_result = llm.invoke(validation_messages)
    iteration += 1

# Extract validation content
if isinstance(validation_result.content, list):
    validation_content = "\n".join([item.get('text', str(item)) if isinstance(item, dict) else str(item) for item in validation_result.content])
else:
    validation_content = str(validation_result.content)

# Compare validation results
validation_matches = re.findall(marks_pattern, validation_content)
original_section_matches = re.findall(marks_pattern, all_section_results[0]['content'])

consistency_check = "PASSED" if len(validation_matches) == len(original_section_matches) else "WARNING"
print(f"Consistency Check: {consistency_check}")
if consistency_check == "WARNING":
    print(f"  Original: {len(original_section_matches)} questions graded")
    print(f"  Validation: {len(validation_matches)} questions graded")

# Create final summary
accurate_summary = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERIFIED FINAL SUMMARY (Python Calculated):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Grading Configuration:
  - Temperature: 0.0 (Maximum Determinism)
  - Seed: {GRADING_SEED} (For Reproducibility)
  - Processing: Section-by-Section
  - Validation: {consistency_check}

Total Questions Graded: {len(question_scores)}
Total Marks Obtained: {total_obtained:.1f}
Total Marks Possible: {total_possible:.1f}
Percentage: {percentage:.2f}%
Grade: {grade}

Question-wise Score Summary:
"""

for idx, (obtained, possible) in enumerate(question_scores, 1):
    accurate_summary += f"  Question {idx}: {obtained:.1f}/{possible:.1f}\n"

# Format final output
output = []
output.append("\n" + "="*100)
output.append("EXAM GRADING REPORT".center(100))
output.append("="*100)
output.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
output.append(f"Exam: Physics")
output.append(f"Marking Scheme: {marking_scheme_file_path}")
output.append(f"Total Pages Processed: {len(l)}")
output.append("-"*100)
output.append("\n" + combined_content)
output.append(accurate_summary)
output.append("\n" + "="*100)

# Print to console
formatted_output = "\n".join(output)
print(formatted_output)

# Save to file
output_filename = f"grading_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(formatted_output)

print(f"\n✓ Grading complete! Results saved to: {output_filename}")
print(f"✓ Configuration: Temperature=0.0, Seed={GRADING_SEED}, Validation={consistency_check}")
