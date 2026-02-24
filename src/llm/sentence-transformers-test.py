from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("sentence-transformers/paraphrase-mpnet-base-v2")
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

texts = ["RAG is powerful", "Embeddings convert text to vectors"]
embeddings = model.encode(texts)

print(len(embeddings[0]))