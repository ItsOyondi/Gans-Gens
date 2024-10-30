import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import faiss
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to read continuous text from a file and split into chunks
def read_documents_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        # Split text by full stops and filter empty chunks
        documents = [sentence.strip() for sentence in text.split('.') if sentence.strip()]
    return documents

# Load documents from the text file
documents = read_documents_from_file("transcription.txt")  # Specify your file name here

# Create embeddings for the documents using Sentence-BERT
def encode_documents(docs):
    embeddings = model.encode(docs, convert_to_tensor=True)
    return embeddings.numpy()

# Create FAISS index
document_embeddings = encode_documents(documents)
dimension = document_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(document_embeddings.astype('float32'))

# Function to retrieve relevant documents
def retrieve_documents(query, k=2):
    query_embedding = model.encode([query], convert_to_tensor=True).numpy()
    distances, indices = index.search(query_embedding.astype('float32'), k)
    return indices[0], distances[0]

# Function to generate an answer using GPT-2
def generate_answer(query):
    indices, _ = retrieve_documents(query)
    retrieved_docs = [documents[i] for i in indices]
    
    # Create context for GPT-2
    context = " ".join(retrieved_docs)
    input_text = f"Context: {context}\nQuestion: {query}\nAnswer:"
    
    # Load GPT-2 model and tokenizer for generating answers
    from transformers import GPT2Tokenizer, GPT2LMHeadModel

    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    gpt_model = GPT2LMHeadModel.from_pretrained("gpt2")
    gpt_model.eval()

    # Generate answer
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    with torch.no_grad():
        output = gpt_model.generate(input_ids, max_new_tokens=50, num_return_sequences=1)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return answer

# Example usage
if __name__ == "__main__":
    query = "How many years your child can spend in 4th grade?"
    answer = generate_answer(query)
    print(answer)
