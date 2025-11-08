from langchain.agents import create_agent
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
import pprint
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma
import base64
from langchain.messages import HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools import tool

os.environ["GEMINI_API_KEY"] = "AIzaSyDPGFLcb_iuSj27IW32YSMYQYDadrppG9s"
os.environ["GOOGLE_API_KEY"] = "AIzaSyDPGFLcb_iuSj27IW32YSMYQYDadrppG9s"


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store = Chroma(
    collection_name="exam_sheet_evaluator",
    embedding_function=embeddings,
    persist_directory="./memory_vector_database",  
)

file_path = "./example_data/markingscheme.pdf"
loader = PyMuPDF4LLMLoader(file_path)
docs = loader.load()
#pprint.pp(docs[0].metadata)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  #(characters)
    chunk_overlap=200,  # (characters)
    add_start_index=True,  
)

all_splits = text_splitter.split_documents(docs)
document_ids = vector_store.add_documents(documents=all_splits)

#print(document_ids[:3])

@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    tools = [get_weather]
)

SYSTEM_PROMPT='''
you are a professor in Delhi Technological University who has been assigned to grade these exam sheets pdf.
you have to grade this pdf based on factual accuracy, accuracy and whatever else is needed for grading.
you have to also refer the given answer key pdf for directions on what is expected in the answer.  you can also search the internet if needed.

'''

image_file_path = "hq720.jpg"

with open(image_file_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

message_local = HumanMessage(
    content=[
        {"type": "text", "text": f"{SYSTEM_PROMPT}"},
        {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image}"},
    ]
)
result_local = llm.invoke([message_local])
print(f"Response for local image: {result_local.content}")
