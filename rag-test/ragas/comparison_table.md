# TechCorp — RAGAS Evaluation

LLM-as-judge metrics. Faith = Faithfulness, Correct = Answer Correctness, Recall = Context Recall, Precision = Context Precision.


## run_009 — 2026-06-23 13:27 | chat: meta-llama/llama-4-scout-17b-16e-instruct | judge: meta-llama/llama-4-scout-17b-16e-instruct
**Avg: Faith=1.0 | Correct=None | Recall=1.0 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q01 | easy | exact_match | 1.00 | — | 1.00 | 1.00 | ❌ |
| Q02 | easy | exact_match | 1.00 | — | 1.00 | 1.00 | ❌ |
| Q03 | easy | exact_match | 1.00 | — | 1.00 | 1.00 | ❌ |

## run_010 — 2026-06-23 13:28 | chat: meta-llama/llama-4-scout-17b-16e-instruct | judge: meta-llama/llama-4-scout-17b-16e-instruct
**Avg: Faith=1.0 | Correct=0.8547 | Recall=1.0 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q01 | easy | exact_match | 1.00 | 0.98 | 1.00 | 1.00 | ✅ |
| Q02 | easy | exact_match | 1.00 | 0.60 | 1.00 | — | ❌ |
| Q03 | easy | exact_match | — | 0.98 | 1.00 | — | ❌ |

## run_011 — 2026-06-23 13:41 | chat: meta-llama/llama-4-scout-17b-16e-instruct | judge: meta-llama/llama-4-scout-17b-16e-instruct
**Avg: Faith=1.0 | Correct=0.8974 | Recall=1.0 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q01 | easy | exact_match | 1.00 | 0.98 | 1.00 | 1.00 | ✅ |
| Q02 | easy | exact_match | 1.00 | 0.97 | 1.00 | 1.00 | ✅ |
| Q03 | easy | exact_match | 1.00 | 0.98 | 1.00 | 1.00 | ✅ |
| Q04 | easy | named_entity | 1.00 | 0.82 | 1.00 | 1.00 | ✅ |
| Q05 | easy | named_entity | 1.00 | 0.73 | 1.00 | 1.00 | ✅ |

## run_013 — 2026-06-23 14:05 | chat: llama-3.3-70b-versatile | judge: openai/gpt-oss-120b
**Avg: Faith=0.8438 | Correct=0.6962 | Recall=0.9375 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q02 | easy | exact_match | 1.00 | 0.97 | 1.00 | 1.00 | ✅ |
| Q06 | easy | direct_fact | 1.00 | 0.97 | 1.00 | 1.00 | ✅ |
| Q11 | medium | paraphrase | 1.00 | 0.18 | 1.00 | 1.00 | ❌ |
| Q16 | medium | distractor | 0.50 | 0.57 | 1.00 | 1.00 | ❌ |
| Q21 | medium | multi_chunk | 1.00 | 0.67 | 1.00 | 1.00 | ✅ |
| Q25 | medium | inference | 0.75 | 0.88 | 1.00 | 1.00 | ❌ |
| Q28 | medium | negation | 1.00 | 0.60 | 1.00 | 1.00 | ❌ |
| Q31 | hard | adversarial_paraphrase | 0.50 | 0.72 | 0.50 | 1.00 | ❌ |
| Q33 | hard | absent_plausible | — | — | — | — | ⏭️ — |

## run_015 — 2026-06-23 15:13 | chat: llama-3.3-70b-versatile | judge: openai/gpt-oss-120b
**Avg: Faith=1.0 | Correct=0.1862 | Recall=1.0 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q11 | medium | paraphrase | 1.00 | 0.19 | 1.00 | 1.00 | ❌ |

## run_016 — 2026-06-23 15:24 | chat: llama-3.3-70b-versatile | judge: openai/gpt-oss-120b
**Avg: Faith=1.0 | Correct=0.5497 | Recall=1.0 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q11 | medium | paraphrase | 1.00 | 0.55 | 1.00 | 1.00 | ❌ |

## run_017 — 2026-06-23 15:26 | chat: llama-3.3-70b-versatile | judge: openai/gpt-oss-120b
**Avg: Faith=1.0 | Correct=0.7245 | Recall=1.0 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q28 | medium | negation | 1.00 | 0.72 | 1.00 | 1.00 | ✅ |

## run_018 — 2026-06-23 15:29 | chat: llama-3.3-70b-versatile | judge: openai/gpt-oss-120b
**Avg: Faith=0.75 | Correct=0.8423 | Recall=1.0 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q25 | medium | inference | 0.75 | 0.84 | 1.00 | 1.00 | ❌ |

## run_019 — 2026-06-23 15:30 | chat: llama-3.3-70b-versatile | judge: openai/gpt-oss-120b
**Avg: Faith=0.5 | Correct=None | Recall=0.5 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q31 | hard | adversarial_paraphrase | 0.50 | — | 0.50 | 1.00 | ❌ |

## run_020 — 2026-06-23 15:32 | chat: llama-3.3-70b-versatile | judge: openai/gpt-oss-120b
**Avg: Faith=None | Correct=None | Recall=None | Precision=None**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q31 | hard | adversarial_paraphrase | — | — | — | — | ❌ |

## run_021 — 2026-06-23 15:36 | chat: llama-3.3-70b-versatile | judge: openai/gpt-oss-120b
**Avg: Faith=None | Correct=None | Recall=None | Precision=None**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q31 | hard | adversarial_paraphrase | — | — | — | — | ❌ |

## run_022 — 2026-06-23 15:42 | chat: llama-3.3-70b-versatile | judge: gpt-oss-120b
**Avg: Faith=1.0 | Correct=0.8302 | Recall=0.5 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q31 | hard | adversarial_paraphrase | 1.00 | 0.83 | 0.50 | 1.00 | ✅ |

## run_023 — 2026-06-23 15:48 | chat: llama-3.3-70b-versatile | judge: gpt-oss-120b
**Avg: Faith=None | Correct=0.6501 | Recall=0.5 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q31 | hard | adversarial_paraphrase | — | 0.65 | 0.50 | 1.00 | ❌ |

## run_025 — 2026-06-23 16:02 | chat: llama-3.3-70b-versatile | judge: gpt-oss-120b
**Avg: Faith=0.5 | Correct=0.1935 | Recall=1.0 | Precision=1.0**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q16 | medium | distractor | 0.50 | 0.19 | 1.00 | 1.00 | ❌ |

## run_026 — 2026-06-24 08:31 | chat: llama-3.3-70b-versatile | judge: openai/gpt-oss-120b
**Avg: Faith=1.0 | Correct=0.5365 | Recall=0.5833 | Precision=0.5972**

| Q | Diff | Category | Faith | Correct | Recall | Precision | Status |
|---|---|---|---|---|---|---|---|
| Q27 | medium | negation | 1.00 | 0.98 | 1.00 | 1.00 | ✅ |
| Q28 | medium | negation | 1.00 | 0.12 | 0.00 | 0.00 | ❌ |
| Q29 | medium | ambiguous | 1.00 | 0.43 | 1.00 | 1.00 | ❌ |
| Q30 | medium | ambiguous | 1.00 | 0.67 | 1.00 | 0.58 | ✅ |
| Q31 | hard | adversarial_paraphrase | 1.00 | 0.83 | 0.50 | 1.00 | ✅ |
| Q32 | hard | adversarial_paraphrase | 1.00 | 0.19 | 0.00 | 0.00 | ❌ |
| Q33 | hard | absent_plausible | — | — | — | — | ⏭️ — |
| Q34 | hard | absent_plausible | — | — | — | — | ⏭️ — |

**Notes:**
- Q28: Embedding API returned error during rag_search ("Retrieval unavailable: embedding error."). Transient infrastructure failure — model had no context and defaulted to "not found". Needs re-run.
- Q32: Retrieval failure caused by adversarial vocabulary. Question asked about $500 expense pre-approval (Section 8) but terms like "spending level", "clearance", "outlay" pulled Section 5.4 (professional development budget) instead. Model answered the wrong question.
- Q29: Model returned correct figure ($2,000) but omitted usage details (conferences, courses, etc.).
- Q30: Retrieval ranked Performance Reviews chunk above the correct Salary chunk (precision=0.58).
