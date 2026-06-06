# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain
Student-generated reviews of CS professors. This system helps students understand teaching style, exam difficulty, workload, and grading fairness, which are not clearly described in official course catalogs.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | prof1.txt |local file|docs/prof1.txt |
| 2 | prof2.txt |local file |docs/prof2.txt |
| 3 | prof3.txt |local file |docs/prof3.txt |
| 4 | prof4.txt|local file |docs/prof4.txt |
| 5 | prof5.txt|local file|docs/prof5.txt |
| 6 | prof6.txt|local file|docs/prof6.txt|
| 7 | prof7.txt|local file|docs/prof7.txt|
| 8 | prof8.txt|local file |docs/prof8.txt|
| 9 | prof9.txt |local file |docs/prof9.txt|
| 10 | prof10.txt |local file |docs/prof10.txt|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:**
Professor reviews are short, opinion-based text entries. A smaller chunk size preserves important details like teaching style, exam difficulty, and workload without mixing unrelated ideas. Overlap ensures that key information is not lost when it appears near chunk boundaries.

**Final chunk count:** 87

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 (sentence-transformers)

**Production tradeoff reflection:**
If deployed in production, larger embedding models could improve semantic understanding and support multilingual queries. However, they would be slower and more expensive. This model was chosen because it is lightweight, runs locally, and performs well for small text retrieval tasks like professor reviews.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** 
The system uses Groq’s `llama-3.3-70b-versatile` model to generate answers based ONLY on retrieved chunks.

**How source attribution is surfaced in the response:**
Each retrieved chunk comes from a specific file. These file names act as implicit source attribution and indicate where the information came from.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which professor has easy exams?|Smith or Davis |Professor Davis is described as having fair and manageable exams |Relevant |Accurate |
| 2 |Which professor is hardest? | Brown or Wilson|Professor Brown has the most difficult exams and strict grading |Relevant |Accurate |
| 3 |Which professor is best for beginners? | Davis|Davis is recommended for beginners due to clear explanations |Relevant |Accurate |
| 4 |Which professor gives most homework? |Wilson or Brown |Wilson is described as heavy workload with frequent assignments |Relevant |Accurate |
| 5 |Which professor is most helpful? | Taylor or Anderson|Taylor and Anderson both provide helpful feedback and support |Relevant |Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which professor gives the easiest exams?
**What the system returned:**
It returned mixed chunks mentioning multiple professors instead of one clear answer.
**Root cause (tied to a specific pipeline stage):**
Retrieval stage, multiple chunks contained similar keywords like “exams,” causing irrelevant or mixed results to be returned.
**What you would change to fix it:**
Improve chunking or add reranking so that the system prioritizes professor-specific context instead of generic exam mentions.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The planning document helped define the chunking strategy and retrieval pipeline before coding, which made implementation structured and easier to debug step-by-step. It also clarified how many documents and evaluation questions were required.
**One way your implementation diverged from the spec, and why:**
The system initially did not include full LLM-based grounded generation. It focused only on retrieval due to simplicity and time constraints, but the structure allows Groq integration later if needed.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* Error about missing docs folder and project structure
- *What it produced:* Suggested fixing folder name mismatch and directory structure
- *What I changed or overrode:* Renamed folder to match expected "docs" path

**Instance 2**

- *What I gave the AI:* Chunking strategy section from planning.md
- *What it produced:* Python implementation of chunking logic
- *What I changed or overrode:* Adjusted file paths and ensured compatibility with my local setup

## Query Interface

The system provides a simple Gradio-based web interface for querying the Unofficial Guide.

### How it works:

- User enters a question in a text box
- System retrieves top 5 relevant chunks from ChromaDB
- Groq LLM generates a grounded response using only those chunks
- Both the answer and retrieved sources are displayed

### UI Implementation:

Built using `gradio`, launched with:

```python
demo.launch()

---
