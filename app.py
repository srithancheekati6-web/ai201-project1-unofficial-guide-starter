import os
import gradio as gr
import chromadb
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


client_llm = Groq(api_key=os.getenv("GROQ_API_KEY"))


client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="reviews")


# Retrieval

def retrieve(question):
    results = collection.query(
        query_texts=[question],
        n_results=5
    )

    chunks = results["documents"][0]
    sources = results["metadatas"][0]

    return chunks, sources


# Generation (STRICT grounding)

def generate_answer(question, chunks, sources):

    context = "\n\n".join(chunks)

    prompt = f"""
You are a STRICT grounded assistant.

RULES:
- Use ONLY the context below.
- If the answer is not in the context, say:
  "I don't have enough information in the documents."
- Do NOT use outside knowledge.

CONTEXT:
{context}

QUESTION:
{question}

Return a short, clear answer.

At the end, list sources used (from metadata).
Sources:
{sources}
"""

    response = client_llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# Full pipeline

def ask(question):
    chunks, sources = retrieve(question)
    answer = generate_answer(question, chunks, sources)

    return answer, "\n\n".join(chunks), str(sources)

# UI

demo = gr.Interface(
    fn=ask,
    inputs=gr.Textbox(label="Ask a question"),
    outputs=[
        gr.Textbox(label="Answer"),
        gr.Textbox(label="Retrieved Chunks"),
        gr.Textbox(label="Sources")
    ],
    title="The Unofficial Guide (RAG System)"
)

demo.launch()