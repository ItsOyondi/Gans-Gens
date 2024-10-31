import os
import faiss
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Set environment variable for OpenMP compatibility
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load the sentence transformer model for embedding
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FLAN-T5 model and tokenizer for answer generation
t5_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
t5_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")

# Function to read continuous text from a file and split into chunks
def read_documents_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        # Split text by full stops and filter out empty chunks
        documents = [sentence.strip() for sentence in text.split('.') if sentence.strip()]
    return documents

# Load documents from the specified text file
documents = read_documents_from_file("transcription_old.txt")  # Specify your file name here

# Create embeddings for the documents using Sentence-BERT
def encode_documents(docs):
    embeddings = sentence_model.encode(docs, convert_to_tensor=True)
    return embeddings.cpu().numpy()  # Ensure compatibility with FAISS (CPU)

# Create FAISS index with document embeddings
document_embeddings = encode_documents(documents)
dimension = document_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(document_embeddings.astype('float32'))

# Function to retrieve relevant documents based on the query
def retrieve_documents(query, k=2):
    query_embedding = sentence_model.encode([query], convert_to_tensor=True).cpu().numpy()
    distances, indices = index.search(query_embedding.astype('float32'), k)
    return indices[0], distances[0]

# Function to generate an answer using FLAN-T5
def generate_answer(query):
    indices, _ = retrieve_documents(query)
    retrieved_docs = [documents[i] for i in indices]
    
    # Prepare context for FLAN-T5
    context = " ".join(retrieved_docs)
    input_text = f"Context: {context} Question: {query}"

    # Generate answer using FLAN-T5
    input_ids = t5_tokenizer.encode(input_text, return_tensors='pt')
    with torch.no_grad():
        output = t5_model.generate(input_ids, max_new_tokens=50, num_return_sequences=1)
    answer = t5_tokenizer.decode(output[0], skip_special_tokens=True)
    
    return answer

# Example usage
if __name__ == "__main__":
    query = "Who are the main people mentioned in the text?"
    answer = generate_answer(query)
    print(answer)
