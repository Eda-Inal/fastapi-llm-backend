# RAG Test Results

Test date: 2026-06-02  
Embedding model: mxbai-embed-large (Ollama, 1024-dim)  
Hybrid search: enabled (dense + BM25 + RRF)  
Reranker: enabled (jina-reranker-v2-base-multilingual)

---

## Key Findings

- `rag_search` is only triggered when the question explicitly references the user's own documents using phrases like "my documents / my files / my uploaded documents".
- Without these phrases, the model falls back to `web_search` or answers directly from general knowledge.
- No hallucinations observed on questions whose answers are not in the documents — the model honestly returns "not found".
- Table chunks are preserved atomically and comparison queries work correctly.

---

## Test 1 — Aurora Research Station (aurora_station.txt)

**document_id:** 34 | **chunks:** 3 | **tokens:** 678

### 1A — Without "my documents" phrasing (llama-3.3-70b-versatile)

| # | Question | Expected Answer | Model | Result |
|---|----------|----------------|-------|--------|
| 1 | When was the station established? | 2018 | llama-3.3-70b-versatile | ❌ web_search triggered (`<\|python_tag\|>` bug) |
| 2 | How many main buildings are there? | 3 | llama-3.3-70b-versatile | ❌ RAG not called, returned "not enough information" |
| 3 | What is stored in the third building? | Data center | llama-3.3-70b-versatile | ✅ RAG triggered correctly |
| 4 | How many wind turbines are used? | 6 | llama-3.3-70b-versatile | ❌ web_search, unrelated result |
| 5 | How often do supply shipments arrive? | Every six weeks | llama-3.3-70b-versatile | ❌ web_search, returned Amazon shipping info |
| 6 | How many birds have been tracked since 2019? | More than 1,500 | llama-3.3-70b-versatile | ❌ web_search, unrelated result |
| 7 | What is the name of the island? | Not in document | llama-3.3-70b-versatile | ❌ web_search triggered (`<\|python_tag\|>` bug) |
| 8 | What is the annual budget of the station? | Not in document | llama-3.3-70b-versatile | ❌ web_search, hallucinated a radio station budget |
| 9 | Could the station survive two months without supply shipments? | Yes (3-month reserves) | llama-3.3-70b-versatile | ✅ RAG triggered, correct inference |
| 10 | Is renewable energy the main power source? | Yes | llama-3.3-70b-versatile | ❌ web_search, returned global energy statistics |

**Score: 2/10** — Routing is unreliable without explicit document reference phrases.

---

### 1B — With "my documents" phrasing (llama-3.3-70b-versatile)

| # | Question | Expected Answer | Model | Result |
|---|----------|----------------|-------|--------|
| 1 | According to my documents, when was the station established? | 2018 | llama-3.3-70b-versatile | ✅ "The station was established in 2018." |
| 2 | In my uploaded files, how many main buildings are there? | 3 | llama-3.3-70b-versatile | ✅ "There are three main buildings." |
| 3 | According to my documents, what is stored in the third building? | Data center | llama-3.3-70b-versatile | ✅ "A large data center that processes and stores research findings." |
| 4 | In my files, how many wind turbines are used? | 6 | llama-3.3-70b-versatile | ✅ "Six wind turbines." |
| 5 | According to my documents, how often do supply shipments arrive? | Every six weeks | llama-3.3-70b-versatile | ✅ "Every six weeks." |
| 6 | In my uploaded documents, how many birds have been tracked since 2019? | More than 1,500 | llama-3.3-70b-versatile | ✅ "More than 1,500 birds." |
| 7 | According to my documents, what is the name of the island? | Not in document | llama-3.3-70b-versatile | ✅ "This information was not found in your documents." |
| 8 | In my files, what is the annual budget of the station? | Not in document | llama-3.3-70b-versatile | ✅ "This information was not found in your documents." |
| 9 | According to my documents, could the station survive two months without supply shipments? | Yes | llama-3.3-70b-versatile | ✅ Correct inference — "up to three months reserve" |
| 10 | In my documents, is renewable energy the main power source? | Yes | llama-3.3-70b-versatile | ✅ Correct inference — wind + solar = primary sources |

**Score: 10/10**

---

### 1C — Unanswerable questions (llama-3.3-70b-versatile)

| # | Question | Model | Result |
|---|----------|-------|--------|
| 1 | According to my documents, which university owns the station? | llama-3.3-70b-versatile | ✅ "Not found in your documents." |
| 2 | In my files, what brand are the wind turbines? | llama-3.3-70b-versatile | ✅ "Not found in your documents." |
| 3 | According to my documents, what species of seabirds are being tracked? | llama-3.3-70b-versatile | ✅ "Not found in your documents." |
| 4 | In my uploaded documents, what programming language is used in the data center software? | llama-3.3-70b-versatile | ✅ "Not found in your documents." |
| 5 | According to my documents, what is the average annual temperature on the island? | llama-3.3-70b-versatile | ✅ "Not found in your documents." |
| 6 | In my files, how many female researchers work at the station? | llama-3.3-70b-versatile | ✅ "Not found in your documents." |

**Score: 6/6** — No hallucinations on any unanswerable question.

---

## Test 2 — GreenTech Solutions Internal Report (greentech_report.md)

**document_id:** 35 | **chunks:** 8 | **tokens:** 422  
Format: markdown with headings, table, and sections.  
Each chunk carries section heading metadata.

### Chunk Structure

| Chunk | Tokens | Section Heading |
|-------|--------|----------------|
| 0 | 6 | GreenTech Solutions Internal Report |
| 1 | 125 | Overview |
| 3 | 34 | Energy Monitor Pro |
| 4 | 29 | PredictAI |
| 5 | 30 | SmartAlert |
| 7 | 61 | Company Offices (table) |
| 9 | 87 | Recent Achievements |
| 10 | 50 | Future Plans |

Note: Chunks 2, 6, 8 were `---` separator lines, correctly dropped by `_drop_tiny_chunks`.

### 2A — Factual questions (llama-3.3-70b-versatile)

| # | Question | Expected | Model | Result |
|---|----------|---------|-------|--------|
| 1 | When was GreenTech Solutions founded? | 2017 | llama-3.3-70b-versatile | ✅ |
| 2 | Where is the company's headquarters located? | Amsterdam, Netherlands | llama-3.3-70b-versatile | ✅ |
| 3 | Approximately how many clients does the company serve? | 350+ | llama-3.3-70b-versatile | ✅ |
| 4 | What is the name of GreenTech's flagship platform? | Energy Monitor Pro | llama-3.3-70b-versatile | ✅ |
| 5 | Which product uses machine learning to forecast energy consumption? | PredictAI | llama-3.3-70b-versatile | ✅ |
| 6 | How many employees work in the Berlin office? | 40 | llama-3.3-70b-versatile | ✅ Correctly retrieved from table chunk |
| 7 | What percentage reduction in dashboard loading times was achieved in 2024? | 45% | llama-3.3-70b-versatile | ✅ |
| 8 | How many IoT sensors were deployed in the company's largest project? | 2,500+ | llama-3.3-70b-versatile | ✅ |
| 9 | What award did GreenTech receive in 2024? | Sustainable Innovation Award | llama-3.3-70b-versatile | ✅ |
| 10 | In which year does the company plan to expand into North America? | 2027 | llama-3.3-70b-versatile | ✅ |

**Score: 10/10**

---

### 2B — Multi-model comparison

| Question | llama-3.3-70b-versatile | qwen/qwen3-32b | openai/gpt-oss-120b:free |
|----------|------------------------|---------------|--------------------------|
| Who is the CEO of GreenTech Solutions? (not in document) | — | ✅ "Not found" | — |
| Which office has more employees: Berlin or Madrid? | — | ✅ Berlin (40) > Madrid (30) | — |
| Which is smaller, Milan or Madrid, and by how many employees? | — | ❌ web_search triggered, returned jll.com result | ✅ Milan (20) < Madrid (30), difference: 10 |

**Routing observations:**
- `llama-3.3-70b-versatile` — consistently follows the "my documents" routing rule.
- `qwen/qwen3-32b` — ignored the routing prompt on a comparison query and fell back to web_search.
- `openai/gpt-oss-120b:free` — routing consistent, correctly retrieved and compared table values.

---

## Test 3 — llama-3.1-8b-instant (Small Model)

Mixed questions across both documents. 3 second delay between requests to stay under TPM limit (6,000 TPM).

### 3A — Factual + unanswerable questions

| # | Question | Expected | Result |
|---|----------|---------|--------|
| 1 | How many countries have researchers visited the Aurora Research Station from? | 18 | ✅ "18 countries" |
| 2 | What does PredictAI use to forecast energy consumption? | Machine learning models | ✅ Correct, returned section heading too |
| 3 | How many water sample locations does the Aurora station monitor for ocean acidity? | 25 | ✅ "25 water sample locations" |
| 4 | What is the wifi password at the Aurora Research Station? (not in document) | Not found | ✅ "Not found in your documents." |
| 5 | Who founded GreenTech Solutions? (not in document — only "a group of environmental scientists") | Not found | ✅ "Not found in your documents." |

**Score: 5/5**

### 3B — Unanswerable questions (hallucination check)

| # | Question | Expected | Result |
|---|----------|---------|--------|
| 1 | What is the salary of the researchers at the Aurora Research Station? | Not found | ✅ "Not found in your documents." |
| 2 | What is the stock price of GreenTech Solutions? | Not found | ⚠️ "Not found" correct, but leaked `<function=web_search>` as plain text |

**Score: 2/2 correct answers, but instruction following issue on Q2.**

**Observation:** "Stock price" phrasing triggered the model's web_search instinct even during finalization. The RAG answer was correct but the model leaked a web_search call as plain text instead of staying silent. This is an instruction-following weakness in smaller models — `FINALIZATION_SYSTEM_MESSAGE`'s "do not write function calls as text" rule was not fully respected.

**Recommended testing strategy:**
- Use `llama-3.1-8b-instant` for initial test passes (cheap, fast, ~300 tokens/query)
- If 8b gives a wrong or unexpected answer, re-run with a larger model to distinguish:
  - **Retrieval failure** → wrong chunks returned → large model also fails → fix chunking/embeddings
  - **Instruction following failure** → correct chunks but model ignored them → large model succeeds → 8b limitation

---

## Summary

| Metric | Result |
|--------|--------|
| Routing without "my documents" phrasing | Unreliable — falls back to web_search |
| Routing with "my documents" phrasing | Reliable (llama, gpt-oss) |
| Hallucinations on unanswerable questions | None |
| Data retrieval from table chunks | Working correctly |
| Inference-based questions | Working correctly |
| Markdown section heading metadata | Visible in answers as `(section X)` |
| Most consistent routing model | llama-3.3-70b-versatile, openai/gpt-oss-120b:free |
| Routing issue observed | qwen/qwen3-32b |
| Small model (8b) retrieval accuracy | 7/7 correct |
| Small model (8b) instruction following | Weak on real-time query phrasing ("stock price") — leaks function call syntax |
