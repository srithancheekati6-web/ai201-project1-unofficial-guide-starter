import os
import gradio as gr
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# -----------------------
# Load Groq LLM
# -----------------------
client_llm = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load embedding model

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load ChromaDB

client = chromadb.Client()
collection = client.get_collection("reviews")

# Retrieval function

def retrieve(question):
    results = collection.query(
        query_texts=[question],
        n_results=5
    )

    chunks = results["documents"][0]
    return chunks

# Generation (GROQ)

def generate_answer(question, chunks):

    context = "\n\n".join(chunks)

    prompt = f"""
You are a strict assistant.

Answer ONLY using the context below.
If the answer is not in the context, say:
"I don't have enough information in the documents."

Context:
{context}

Question:
{question}

Return a clear, short answer.
Also mention which document chunks support your answer.
"""

    response = client_llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# FULL PIPELINE

def ask(question):

    chunks = retrieve(question)

    answer = generate_answer(question, chunks)

    return answer, "\n\n".join(chunks)


# GRADIO UI

demo = gr.Interface(
    fn=ask,
    inputs="text",
    outputs=["text", "text"],
    title="The Unofficial Guide (RAG System)"
)

demo.launch()