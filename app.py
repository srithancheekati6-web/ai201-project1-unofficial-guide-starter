import os
import chromadb
import gradio as gr

from sentence_transformers import SentenceTransformer

# Load documents

documents = []

sources = []

for file in os.listdir("docs"):
    if file.endswith(".txt"):
        with open(
            os.path.join("docs", file),
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

            documents.append(text)

            sources.append(file)

# Chunking

chunks = []

chunk_sources = []

for doc, source in zip(documents, sources):

    for i in range(0, len(doc), 250):

        chunk = doc[i:i+300]

        chunks.append(chunk)

        chunk_sources.append(source)

# Embeddings

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(
    chunks
)

# ChromaDB

client = chromadb.Client()

collection = client.create_collection(
    "reviews"
)

collection.add(
    documents=chunks,
    ids=[str(i) for i in range(len(chunks))]
)

def ask(question):

    results = collection.query(
        query_texts=[question],
        n_results=5
    )

    retrieved = results["documents"][0]

    answer = "\n\n".join(retrieved)

    return answer

demo = gr.Interface(
    fn=ask,
    inputs="text",
    outputs="text"
)

demo.launch()