# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

This project uses professor reviews collected from RateMyProfessors-style feedback.  
This information is useful because students often rely on peer reviews to choose classes, but official course catalogs do not include details like teaching style, exam difficulty, or grading fairness.  

This makes it a strong use case for a RAG system because the information is text-heavy, subjective, and spread across multiple sources.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | prof1.txt  |Professor Smith review | local file|
| 2 | prof2.txt  |Professor Johnson review| local file|
| 3 | prof3.txt  |Professor Brown review | local file|
| 4 | prof4.txt  | Professor Davis review| local file|
| 5 | prof5.txt  |Professor Wilson review | local file|
| 6 | prof6.txt  |Professor Taylor review | local file|
| 7 | prof7.txt  |Professor Martinez review | local file|
| 8 | prof8.txt  |Professor Anderson review | local file|
| 9 | prof9.txt  |Professor Thomas review| local file|
| 10 | prof10.txt  |Professor White revie | local file|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 300 characters 

**Overlap:** 50 characters  

**Reasoning:**
Professor reviews are short and opinion-based, so smaller chunks help preserve meaning and ensure that important details like exam difficulty, grading style, and workload are not split apart. The overlap helps maintain context between chunks when sentences span boundaries.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 (sentence-transformers)

**Top-k:** 5

**Production tradeoff reflection:**
If this were deployed in a real system, I would consider using a larger embedding model for better semantic understanding, especially for nuanced student opinions. However, larger models increase latency and cost. The current model is chosen because it is fast, lightweight, and sufficient for small-to-medium text retrieval tasks like professor reviews.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |Which professor has the easiest exams? |Professor Smith or Davis |
| 2 | Which professor is the most difficult?| Professor Brown or Wilson|
| 3 | Which professor is best for beginners?  |Professor Davis |
| 4 | Which professor gives the most workload? |Professor Wilson or Brown |
| 5 | Which professor is most helpful in office hours? | Professor Taylor or Anderson|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.  Some reviews may contain mixed or conflicting opinions, which could make retrieval less consistent across chunks.

2. Important information (like exam difficulty or workload) may be split across chunks, causing partial or incomplete answers during retrieval.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
Document Files (prof1–prof10.txt)  
        ↓  
Chunking (300 chars + 50 overlap)  
        ↓  
Embedding (all-MiniLM-L6-v2)  
        ↓  
Vector Store (ChromaDB)  
        ↓  
Retrieval (Top-5 similar chunks)  
        ↓  
Response Output (Gradio Interface)
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:** 
I will use ChatGPT to help implement file loading and chunking logic. I will provide the chunk size and overlap values from this document and ask it to generate Python functions that split documents correctly.

**Milestone 4 — Embedding and retrieval:**
I will use ChatGPT and documentation from sentence-transformers to implement embedding generation and ChromaDB storage. I will verify correctness by checking that queries return relevant professor reviews.
**Milestone 5 — Generation and interface:**
I will use ChatGPT to help build the Gradio interface and connect the retrieval pipeline to a simple question-answering function. I will test the system by running evaluation questions and confirming expected outputs appear in retrieved chunks.