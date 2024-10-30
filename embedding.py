# import numpy as np
# import faiss
# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# from sentence_transformers import SentenceTransformer

# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# model = GPT2LMHeadModel.from_pretrained("gpt2")
# model.eval()

# def embed_data(file_path, index_path, model, k):
#     with open(file_path, "r") as f:
#         texts = [line.strip() for line in f]

#     model = SentenceTransformer(model) 
#     vectors = model.encode(texts, convert_to_tensor=False) 
#     vectors = np.array(vectors).astype("float32")
#     # Determine the Dimension of the Embeddings
#     dimension = vectors.shape[1]
#     index = faiss.IndexFlatL2(dimension) 
#     index.add(vectors) # Add Embeddings to the Index
#     faiss.write_index(index, index_path)
#     # To test the search, we can use the embedding of the first text line as a query
#     query_vector = vectors[0].reshape(1, -1)
#     distances, indices = index.search(query_vector, k)

#     print("Distances:", distances)
#     print("Indices:", indices)
#     print("Finished embedding")

# def encode_documents(docs):
#     inputs = tokenizer(docs, return_tensors='pt', padding=True, truncation=True)
#     with torch.no_grad():
#         embeddings = model.transformer.wte(inputs.input_ids).mean(dim=1).numpy()
#     return embeddings
# # if __name__ == "__main__":
# #     file_path = "transcription.txt"  
# #     model = "all-MiniLM-L6-v2"
# #     k = 5
# #     index_path = "text_vector_index.faiss" 

# #     # Correct the order of arguments here
# #     embed_data(file_path, index_path, model, k)
