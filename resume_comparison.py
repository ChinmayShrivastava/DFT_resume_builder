import pinecone
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize Pinecone
pinecone.init(api_key='your-api-key', environment='us-west1-gcp')
index = pinecone.Index('resume-index')

# Load the Sentence-BERT model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def compare_resume(user_resume_sections):
    suggestions = {}
    for section_label, user_section_text in user_resume_sections.items():
        # Convert user section text to vector
        user_vector = model.encode(user_section_text)
        # Query Pinecone for similar standard resume sections
        query_results = index.query(queries=[user_vector], top_k=5)
        for result in query_results['results']:
            for match in result['matches']:
                # Calculate cosine similarity
                cos_sim = np.dot(user_vector, match['vector']) / (np.linalg.norm(user_vector) * np.linalg.norm(match['vector']))
                # Generate suggestions based on similarity
                if cos_sim < 0.8:  # Assuming a threshold for similarity
                    suggestions[section_label] = {
                        'similarity': cos_sim,
                        'suggestions': generate_suggestions(user_section_text, match['metadata'])
                    }
    return suggestions

def generate_suggestions(user_text, standard_metadata):
    # This function compares the user's text with the standard metadata and generates suggestions for improvement.
    # For simplicity, we're returning a generic message here. In a real-world application, this function would be more complex.
    return "Consider revising this section to improve clarity and impact."