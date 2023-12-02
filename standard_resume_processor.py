# Import necessary libraries
from sentence_transformers import SentenceTransformer
import pinecone
import json
from gpt_chunker import chunk_sections
from docx import Document
import fitz  # PyMuPDF

# Initialize Pinecone
pinecone.init(api_key='your-api-key', environment='us-west1-gcp')

# Create or connect to an existing Pinecone index
index_name = 'resume-index'
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=768)
index = pinecone.Index(index_name)

# Load the Sentence-BERT model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def read_resume_file(file_path):
    """
    Function to read resume file and extract text
    Supports both DOCX and PDF formats
    """
    if file_path.endswith('.docx'):
        doc = Document(file_path)
        text = ' '.join([p.text for p in doc.paragraphs])
    elif file_path.endswith('.pdf'):
        doc = fitz.open(file_path)
        text = ' '.join([page.getText() for page in doc])
    else:
        raise ValueError("Unsupported file format. Please upload a DOCX or PDF file.")
    return text

def process_standard_resumes(standard_resumes):
    """
    Function to process standard resumes
    """
    for resume in standard_resumes:
        # Read the resume file and extract text
        text = read_resume_file(resume['file_path'])

        # Chunk the resume into sections using GPT
        sections = chunk_sections(text)

        for section_label, section_text in sections.items():
            # Convert section text to vector
            vector = model.encode(section_text)

            # Store the vector in Pinecone with metadata
            index.upsert(vectors=[(resume['metadata']['id'], vector, resume['metadata'])])