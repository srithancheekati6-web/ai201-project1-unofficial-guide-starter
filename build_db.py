import os
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="reviews")

docs_path = "docs"

chunks = []
ids = []
metadatas = []

chunk_size = 300
chunk_id = 0

for file in os.listdir(docs_path):
    file_path = os.path.join(docs_path, file)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
        ids.append(f"{file}_{chunk_id}")
        metadatas.append({"source": file})
        chunk_id += 1

embeddings = model.encode(chunks).tolist()

collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=ids,
    metadatas=metadatas
)

print(f"Loaded {len(chunks)} chunks into ChromaDB.")