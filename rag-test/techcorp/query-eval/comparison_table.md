# TechCorp — Query Quality Eval

Compares routing model's generated query vs modelsiz baseline.
**B** = baseline (user question direct to RAG). **M** = model-generated query.
**Pre/Post** = rank before/after reranker (lower is better).
**Cos** = cosine similarity of correct chunk.
For `absent_plausible`: Pre/Post = top1 score (lower = less false-positive risk).
**Δ** = M − B. ⬆️ improved | ⬇️ worse | 🔴 chunk dropped out of top-5.

## run_001 — 2026-06-22 15:47
**Model:** `meta-llama/llama-4-scout-17b-16e-instruct`  
**recall@5:** 1.0 | **MRR_pre:** 1.0 | **MRR_post:** 1.0  
**⬆️ 0 improved | ➡️ 1 same | ⬇️ 0 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 0 rag_not_called**

| Q | Diff | Category | User Question | Model Query | B.Pre | B.Post | B.Cos | M.Pre | M.Post | M.Cos | Δ Pre | Δ Post | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q01 | easy | exact_match | What must all remote work be conducted over when a… | remote work internal systems access requirements | 1 | 1 | 0.706 | 1 | 1 | 0.707 | ➡️ 0 | ➡️ 0 | ➡️ |

## run_002 — 2026-06-22 16:04
**Model:** `meta-llama/llama-4-scout-17b-16e-instruct`  
**recall@5:** 1.0 | **MRR_pre:** 0.913 | **MRR_post:** 0.968  
**⬆️ 1 improved | ➡️ 29 same | ⬇️ 3 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 1 rag_not_called**

| Q | Diff | Category | User Question | Model Query | B.Pre | B.Post | B.Cos | M.Pre | M.Post | M.Cos | Δ Pre | Δ Post | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q01 | easy | exact_match | What must all remote work be conducted over when a… | remote work internal systems access requirements | 1 | 1 | 0.706 | 1 | 1 | 0.707 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q02 | easy | exact_match | Within how many days must business expenses be sub… | expense management system submission deadline | 1 | 1 | 0.792 | 1 | 1 | 0.714 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q03 | easy | exact_match | How much notice must an employee provide in writin… | notice period for resignation | 1 | 1 | 0.704 | 1 | 1 | 0.692 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q04 | easy | named_entity | What is the email address employees should contact… | email address for lost or stolen device | 1 | 1 | 0.659 | 1 | 1 | 0.571 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q05 | easy | named_entity | What is the home office stipend amount provided to… | home office stipend amount for new employees | 1 | 1 | 0.690 | 1 | 1 | 0.695 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q06 | easy | direct_fact | How long is the vesting period for stock options a… | TechCorp stock options vesting period | 1 | 1 | 0.851 | 1 | 1 | 0.821 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q07 | easy | direct_fact | How many days of paid bereavement leave does TechC… | TechCorp paid bereavement leave days | 1 | 1 | 0.909 | 1 | 1 | 0.902 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q08 | easy | direct_fact | What is the annual professional development budget… | annual professional development budget per employe… | 1 | 1 | 0.595 | 1 | 1 | 0.604 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q09 | easy | dense_primary | When can an employee begin taking parental leave a… | When can an employee begin taking parental leave a… | 1 | 1 | 0.768 | 1 | 1 | 0.767 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q10 | easy | dense_primary | What happens to unexercised stock options after an… | Unexercised stock options after leaving TechCorp | 1 | 1 | 0.805 | 1 | 1 | 0.764 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q11 | medium | paraphrase | How long do employees have to use the new hire wor… | new hire workspace setup allowance usage duration | 1 | 1 | 0.660 | 1 | 1 | 0.658 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q12 | medium | paraphrase | What is the minimum recommended amount of time off… | minimum recommended amount of time off employees s… | 1 | 1 | 0.729 | 1 | 1 | 0.719 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q13 | medium | paraphrase | How long after leaving the company can employees a… | How long after leaving the company can employees a… | 2 | 1 | 0.769 | 2 | 1 | 0.769 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q14 | medium | paraphrase | What connectivity requirement must remote employee… | connectivity requirement for remote employees to w… | 1 | 1 | 0.739 | 1 | 1 | 0.724 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q15 | medium | paraphrase | What must employees do before spending from their … | employees learning and growth budget spending requ… | 1 | 1 | 0.612 | 1 | 1 | 0.581 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q16 | medium | distractor | What is the minimum expense amount that requires a… | minimum expense amount that requires a receipt for… | 1 | 1 | 0.784 | 1 | 1 | 0.783 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q17 | medium | distractor | Which teams may have different in-office expectati… | teams with different in-office expectations | 1 | 1 | 0.598 | 1 | 1 | 0.598 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q18 | medium | distractor | What is the health benefit provided to TechCorp em… | Health benefit provided to TechCorp employees base… | 1 | 1 | 0.838 | 1 | 1 | 0.838 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q19 | medium | distractor | How frequently must managers and employees meet on… | minimum frequency of one-on-one meetings between m… | 1 | 1 | 0.549 | 1 | 1 | 0.536 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q20 | medium | distractor | When do salary adjustments from the annual review … | When do salary adjustments from the annual review … | 1 | 1 | 0.695 | 1 | 1 | 0.685 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q21 | medium | multi_chunk | What happens to an employee's stock options both d… | TechCorp stock options during and after employment… | 1 | 1 | 0.853 | 1 | 1 | 0.850 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q22 | medium | multi_chunk | What security-related obligations must a remote em… | security-related obligations remote employee worki… | 1 | 1 | 0.749 | 1 | 1 | 0.750 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q23 | medium | multi_chunk | What are the combined leave entitlements for an em… | combined leave entitlements for an employee who is… | 2 | 1 | 0.685 | 1 | 2 | 0.690 | ⬆️ -1 | ⬇️ +1 | ⬇️ |
| Q24 | medium | inference | Can a TechCorp employee choose to work from a co-w… | TechCorp employee choose to work from co-working s… | 3 | 1 | 0.812 | 3 | 1 | 0.783 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q25 | medium | inference | Is taking time off considered optional or essentia… | Is taking time off considered optional or essentia… | 1 | 1 | 0.862 | 1 | 1 | 0.862 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q26 | medium | inference | Does disclosing a conflict of interest mean an emp… | *(RAG not called)* | — | — | — | — | — | — | — | — | rag_not_called |
| Q27 | medium | negation | In what situation is an employee not required to s… | situation not required to submit doctor's note for… | 1 | 1 | 0.752 | 1 | 1 | 0.717 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q28 | medium | negation | What information will the IT team never ask an emp… | information IT team will never ask an employee to … | 3 | 1 | 0.610 | 3 | 1 | 0.582 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q29 | medium | ambiguous | How much money does TechCorp allocate per employee… | TechCorp annual budget per employee for career-rel… | 1 | 1 | 0.791 | 1 | 1 | 0.790 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q30 | medium | ambiguous | How often does TechCorp conduct its compensation-r… | TechCorp compensation-related review cycle frequen… | 1 | 1 | 0.796 | 1 | 2 | 0.770 | ➡️ 0 | ⬇️ +1 | ⬇️ |
| Q31 | hard | adversarial_paraphrase | Is there any official guarantee against punishment… | official guarantee against punishment for staff me… | 1 | 2 | 0.611 | 1 | 1 | 0.607 | ➡️ 0 | ⬆️ -1 | ⬆️ |
| Q32 | hard | adversarial_paraphrase | Above what spending level must an employee obtain … | Above what spending level must an employee obtain … | 8 | 1 | 0.633 | 7 | 1 | 0.635 | ⬆️ -1 | ➡️ 0 | ➡️ |
| Q33 | hard | absent_plausible | What notice period or severance pay does TechCorp … | TechCorp notice period or severance pay when letti… | 0.836 | 0.882 | — | 0.817 | 0.802 | — | ➡️ ~0 | ⬆️ -0.080 | ➡️ |
| Q34 | hard | absent_plausible | Does TechCorp offer an annual performance bonus or… | TechCorp annual performance bonus or variable pay | 0.706 | 0.559 | — | 0.753 | 0.548 | — | ⬇️ +0.048 | ➡️ ~0 | ⬇️ |

---

### run_002 Analysis — Scout (`meta-llama/llama-4-scout-17b-16e-instruct`)

**Overall:** recall@5 = 1.0 · MRR_pre = 0.913 · MRR_post = 0.968

The correct chunk landed in the top-5 for all 34 questions. Scout consistently rewrites user questions into shorter keyword phrases; the net impact on retrieval quality is minimal.

#### ⏭️ RAG not called — Q26 (`inference / medium`)
> *"Does disclosing a conflict of interest mean an employee is automatically penalized?"*

Scout answered this question from its own knowledge without invoking RAG at all. The ethical/policy framing likely made it appear answerable without retrieval. No retrieval comparison is possible.

#### ⬆️ Improvement — Q31 (`adversarial_paraphrase / hard`)
> *"Is there any official guarantee against punishment for staff members who speak up?"*

Model query: `"official guarantee against punishment for staff members who speak up"`  
B.Post = **2** → M.Post = **1** (one rank gained after reranker)  
Despite heavy paraphrasing in the question, the model captured the exact semantic core and helped the reranker surface the correct chunk to the top position.

#### ⬇️ Regression — Q23 (`multi_chunk / medium`)
> *"What are the combined leave entitlements for an employee who is…"*

Model query: `"combined leave entitlements for an employee who is…"`  
B.Pre = 2 → M.Pre = **1** (improved in dense stage) but B.Post = 1 → M.Post = **2** (degraded after reranker)  
The model pulled the correct chunk higher in the dense stage, but the reranker preferred a different chunk given the model's query focus. In multi-chunk questions the reranker's choice between two relevant chunks is sensitive to how the query is framed.

#### ⬇️ Regression — Q30 (`ambiguous / medium`)
> *"How often does TechCorp conduct its compensation-related review cycle?"*

Model query: `"TechCorp compensation-related review cycle frequency"`  
B.Post = 1 → M.Post = **2**  
The model condensed the question to a terse keyword phrase; the reranker favors the original question phrasing here. For ambiguous questions the full sentence sometimes provides a stronger reranking signal than a compressed query.

#### ⬇️ Absent false-positive risk increased — Q34 (`absent_plausible / hard`)
> *"Does TechCorp offer an annual performance bonus or variable pay?"*

B.Dense.top1 = 0.706 → M.Dense.top1 = **0.753** (+0.048)  
For a question whose answer does not exist in the knowledge base, the model generated a more focused query that boosted the top-1 similarity score — increasing the risk of a false-positive retrieval hit.

#### Cosine similarity drops (rank unaffected)
| Q | B.Cos | M.Cos | Note |
|---|-------|-------|------|
| Q04 | 0.659 | 0.571 | −0.088 — query over-shortened, but rank held at 1 |
| Q02 | 0.792 | 0.714 | −0.078 — similar compression effect |

Model keyword queries occupy less specific positions in embedding space compared to full question sentences. Ranks are unaffected today, but this compression could become a fragility point on harder or lower-recall questions.

#### Summary

| Outcome | Count | Questions |
|---|---|---|
| ➡️ Same | 29 | — |
| ⬆️ Improved | 1 | Q31 (adversarial_paraphrase) |
| ⬇️ Worse | 3 | Q23, Q30 (rank drop), Q34 (absent risk) |
| ⏭️ RAG not called | 1 | Q26 (inference) |

## run_003 — 2026-06-22 16:11
**Model:** `meta-llama/llama-4-scout-17b-16e-instruct`  
**recall@5:** None | **MRR_pre:** None | **MRR_post:** None  
**⬆️ 0 improved | ➡️ 0 same | ⬇️ 0 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 1 rag_not_called**

| Q | Diff | Category | User Question | Model Query | B.Pre | B.Post | B.Cos | M.Pre | M.Post | M.Cos | Δ Pre | Δ Post | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q01 | easy | exact_match | What must all remote work be conducted over when a… | *(RAG not called)* | — | — | — | — | — | — | — | — | rag_not_called |

## run_004 — 2026-06-22 16:15
**Model:** `meta-llama/llama-4-scout-17b-16e-instruct`  
**recall@5:** 1.0 | **MRR_pre:** 1.0 | **MRR_post:** 1.0  
**⬆️ 0 improved | ➡️ 1 same | ⬇️ 0 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 0 rag_not_called**

| Q | Diff | Category | User Question | Model Query | B.Pre | B.Post | B.Cos | M.Pre | M.Post | M.Cos | Δ Pre | Δ Post | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q01 | easy | exact_match | What must all remote work be conducted over when a… | remote work internal systems access requirements | 1 | 1 | 0.706 | 1 | 1 | 0.707 | ➡️ 0 | ➡️ 0 | ➡️ |

## run_005 — 2026-06-22 16:27
**Model:** `openai/gpt-oss-120b`  
**recall@5:** 1.0 | **MRR_pre:** 1.0 | **MRR_post:** 1.0  
**⬆️ 0 improved | ➡️ 10 same | ⬇️ 0 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 0 rag_not_called**

| Q | Diff | Category | User Question | Model Query | B.Pre | B.Post | B.Cos | M.Pre | M.Post | M.Cos | Δ Pre | Δ Post | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q01 | easy | exact_match | What must all remote work be conducted over when a… | What must all remote work be conducted over when a… | 1 | 1 | 0.706 | 1 | 1 | 0.711 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q02 | easy | exact_match | Within how many days must business expenses be sub… | Within how many days must business expenses be sub… | 1 | 1 | 0.792 | 1 | 1 | 0.794 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q03 | easy | exact_match | How much notice must an employee provide in writin… | notice employee provide in writing before resignin… | 1 | 1 | 0.704 | 1 | 1 | 0.682 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q04 | easy | named_entity | What is the email address employees should contact… | email address employees should contact if their de… | 1 | 1 | 0.659 | 1 | 1 | 0.650 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q05 | easy | named_entity | What is the home office stipend amount provided to… | home office stipend amount new employees | 1 | 1 | 0.690 | 1 | 1 | 0.677 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q06 | easy | direct_fact | How long is the vesting period for stock options a… | How long is the vesting period for stock options a… | 1 | 1 | 0.851 | 1 | 1 | 0.854 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q07 | easy | direct_fact | How many days of paid bereavement leave does TechC… | How many days of paid bereavement leave does TechC… | 1 | 1 | 0.909 | 1 | 1 | 0.909 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q08 | easy | direct_fact | What is the annual professional development budget… | annual professional development budget per employe… | 1 | 1 | 0.595 | 1 | 1 | 0.604 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q09 | easy | dense_primary | When can an employee begin taking parental leave a… | When can an employee begin taking parental leave a… | 1 | 1 | 0.768 | 1 | 1 | 0.767 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q10 | easy | dense_primary | What happens to unexercised stock options after an… | unexercised stock options after employee leaves Te… | 1 | 1 | 0.805 | 1 | 1 | 0.800 | ➡️ 0 | ➡️ 0 | ➡️ |

## run_007 — 2026-06-22 16:40
**Model:** `openai/gpt-oss-120b`  
**recall@5:** 1.0 | **MRR_pre:** 0.95 | **MRR_post:** 1.0  
**⬆️ 0 improved | ➡️ 10 same | ⬇️ 0 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 0 rag_not_called**

| Q | Diff | Category | User Question | Model Query | B.Pre | B.Post | B.Cos | M.Pre | M.Post | M.Cos | Δ Pre | Δ Post | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q11 | medium | paraphrase | How long do employees have to use the new hire wor… | How long do employees have to use the new hire wor… | 1 | 1 | 0.660 | 1 | 1 | 0.648 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q12 | medium | paraphrase | What is the minimum recommended amount of time off… | minimum recommended amount of time off employees s… | 1 | 1 | 0.729 | 1 | 1 | 0.719 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q13 | medium | paraphrase | How long after leaving the company can employees a… | How long after leaving the company can employees a… | 2 | 1 | 0.769 | 2 | 1 | 0.769 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q14 | medium | paraphrase | What connectivity requirement must remote employee… | connectivity requirement remote employees work fro… | 1 | 1 | 0.739 | 1 | 1 | 0.734 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q15 | medium | paraphrase | What must employees do before spending from their … | What must employees do before spending from their … | 1 | 1 | 0.612 | 1 | 1 | 0.612 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q16 | medium | distractor | What is the minimum expense amount that requires a… | minimum expense amount receipt reimbursement | 1 | 1 | 0.784 | 1 | 1 | 0.761 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q17 | medium | distractor | Which teams may have different in-office expectati… | Which teams may have different in-office expectati… | 1 | 1 | 0.598 | 1 | 1 | 0.590 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q18 | medium | distractor | What is the health benefit provided to TechCorp em… | health benefit provided to TechCorp employees base… | 1 | 1 | 0.838 | 1 | 1 | 0.838 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q19 | medium | distractor | How frequently must managers and employees meet on… | How frequently must managers and employees meet on… | 1 | 1 | 0.549 | 1 | 1 | 0.552 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q20 | medium | distractor | When do salary adjustments from the annual review … | When do salary adjustments from the annual review … | 1 | 1 | 0.695 | 1 | 1 | 0.685 | ➡️ 0 | ➡️ 0 | ➡️ |

## run_008 — 2026-06-22 16:51
**Model:** `openai/gpt-oss-120b`  
**recall@5:** 1.0 | **MRR_pre:** 0.817 | **MRR_post:** 1.0  
**⬆️ 0 improved | ➡️ 10 same | ⬇️ 0 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 0 rag_not_called**

| Q | Diff | Category | User Question | Model Query | B.Pre | B.Post | B.Cos | M.Pre | M.Post | M.Cos | Δ Pre | Δ Post | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q21 | medium | multi_chunk | What happens to an employee's stock options both d… | employee stock options during after employment end… | 1 | 1 | 0.853 | 1 | 1 | 0.848 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q22 | medium | multi_chunk | What security-related obligations must a remote em… | security-related obligations remote employee fulfi… | 1 | 1 | 0.749 | 1 | 1 | 0.750 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q23 | medium | multi_chunk | What are the combined leave entitlements for an em… | combined leave entitlements employee ill recently … | 2 | 1 | 0.685 | 2 | 1 | 0.713 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q24 | medium | inference | Can a TechCorp employee choose to work from a co-w… | Can a TechCorp employee choose to work from a co-w… | 3 | 1 | 0.812 | 3 | 1 | 0.804 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q25 | medium | inference | Is taking time off considered optional or essentia… | taking time off optional essential TechCorp | 1 | 1 | 0.862 | 1 | 1 | 0.800 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q26 | medium | inference | Does disclosing a conflict of interest mean an emp… | Does disclosing a conflict of interest mean an emp… | 1 | 1 | 0.728 | 1 | 1 | 0.728 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q27 | medium | negation | In what situation is an employee not required to s… | employee not required to submit a doctor's note fo… | 1 | 1 | 0.752 | 1 | 1 | 0.756 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q28 | medium | negation | What information will the IT team never ask an emp… | What information will the IT team never ask an emp… | 3 | 1 | 0.610 | 3 | 1 | 0.598 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q29 | medium | ambiguous | How much money does TechCorp allocate per employee… | TechCorp allocate per employee annually career-rel… | 1 | 1 | 0.791 | 1 | 1 | 0.789 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q30 | medium | ambiguous | How often does TechCorp conduct its compensation-r… | How often does TechCorp conduct its compensation-r… | 1 | 1 | 0.796 | 1 | 1 | 0.788 | ➡️ 0 | ➡️ 0 | ➡️ |

## run_009 — 2026-06-22 16:56
**Model:** `openai/gpt-oss-120b`  
**recall@5:** 1.0 | **MRR_pre:** 0.562 | **MRR_post:** 1.0  
**⬆️ 2 improved | ➡️ 1 same | ⬇️ 1 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 0 rag_not_called**

| Q | Diff | Category | User Question | Model Query | B.Pre | B.Post | B.Cos | M.Pre | M.Post | M.Cos | Δ Pre | Δ Post | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q31 | hard | adversarial_paraphrase | Is there any official guarantee against punishment… | official guarantee against punishment for staff me… | 1 | 2 | 0.611 | 1 | 1 | 0.607 | ➡️ 0 | ⬆️ -1 | ⬆️ |
| Q32 | hard | adversarial_paraphrase | Above what spending level must an employee obtain … | Above what spending level must an employee obtain … | 8 | 1 | 0.633 | 8 | 1 | 0.633 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q33 | hard | absent_plausible | What notice period or severance pay does TechCorp … | notice period severance pay TechCorp let employee … | 0.836 | 0.882 | — | 0.794 | 0.803 | — | ⬆️ -0.043 | ⬆️ -0.079 | ⬆️ |
| Q34 | hard | absent_plausible | Does TechCorp offer an annual performance bonus or… | TechCorp annual performance bonus variable pay amo… | 0.706 | 0.559 | — | 0.747 | 0.306 | — | ⬇️ +0.041 | ⬆️ -0.253 | ⬇️ |

## run_010 — 2026-06-22 17:11
**Model:** `llama-3.3-70b-versatile`  
**recall@5:** 1.0 | **MRR_pre:** 0.975 | **MRR_post:** 1.0  
**⬆️ 0 improved | ➡️ 20 same | ⬇️ 0 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 0 rag_not_called**

| Q | Diff | Category | User Question | Model Query | B.Pre | B.Post | B.Cos | M.Pre | M.Post | M.Cos | Δ Pre | Δ Post | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q01 | easy | exact_match | What must all remote work be conducted over when a… | remote work internal systems access | 1 | 1 | 0.706 | 1 | 1 | 0.688 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q02 | easy | exact_match | Within how many days must business expenses be sub… | business expenses submission deadline through expe… | 1 | 1 | 0.792 | 1 | 1 | 0.763 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q03 | easy | exact_match | How much notice must an employee provide in writin… | employee notice period in writing before resigning | 1 | 1 | 0.704 | 1 | 1 | 0.706 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q04 | easy | named_entity | What is the email address employees should contact… | email address for lost or stolen device | 1 | 1 | 0.659 | 1 | 1 | 0.571 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q05 | easy | named_entity | What is the home office stipend amount provided to… | home office stipend amount provided to new employe… | 1 | 1 | 0.690 | 1 | 1 | 0.696 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q06 | easy | direct_fact | How long is the vesting period for stock options a… | vesting period for stock options at TechCorp | 1 | 1 | 0.851 | 1 | 1 | 0.838 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q07 | easy | direct_fact | How many days of paid bereavement leave does TechC… | TechCorp paid bereavement leave days | 1 | 1 | 0.909 | 1 | 1 | 0.902 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q08 | easy | direct_fact | What is the annual professional development budget… | annual professional development budget per employe… | 1 | 1 | 0.595 | 1 | 1 | 0.604 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q09 | easy | dense_primary | When can an employee begin taking parental leave a… | When can an employee begin taking parental leave a… | 1 | 1 | 0.768 | 1 | 1 | 0.767 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q10 | easy | dense_primary | What happens to unexercised stock options after an… | unexercised stock options after leaving TechCorp | 1 | 1 | 0.805 | 1 | 1 | 0.764 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q11 | medium | paraphrase | How long do employees have to use the new hire wor… | new hire workspace setup allowance time limit | 1 | 1 | 0.660 | 1 | 1 | 0.619 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q12 | medium | paraphrase | What is the minimum recommended amount of time off… | minimum recommended amount of time off employees s… | 1 | 1 | 0.729 | 1 | 1 | 0.719 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q13 | medium | paraphrase | How long after leaving the company can employees a… | vested equity post-employment | 2 | 1 | 0.769 | 2 | 1 | 0.702 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q14 | medium | paraphrase | What connectivity requirement must remote employee… | remote employees connectivity requirement work fro… | 1 | 1 | 0.739 | 1 | 1 | 0.758 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q15 | medium | paraphrase | What must employees do before spending from their … | learning and growth budget employee spending requi… | 1 | 1 | 0.612 | 1 | 1 | 0.606 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q16 | medium | distractor | What is the minimum expense amount that requires a… | minimum expense amount that requires a receipt for… | 1 | 1 | 0.784 | 1 | 1 | 0.783 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q17 | medium | distractor | Which teams may have different in-office expectati… | teams with different in-office expectations | 1 | 1 | 0.598 | 1 | 1 | 0.598 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q18 | medium | distractor | What is the health benefit provided to TechCorp em… | health benefit provided to TechCorp employees base… | 1 | 1 | 0.838 | 1 | 1 | 0.838 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q19 | medium | distractor | How frequently must managers and employees meet on… | minimum frequency of one-on-one meetings between m… | 1 | 1 | 0.549 | 1 | 1 | 0.536 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q20 | medium | distractor | When do salary adjustments from the annual review … | salary adjustments from the annual review take eff… | 1 | 1 | 0.695 | 1 | 1 | 0.685 | ➡️ 0 | ➡️ 0 | ➡️ |

## run_011 — 2026-06-22 17:21
**Model:** `llama-3.3-70b-versatile`  
**recall@5:** 1.0 | **MRR_pre:** 0.852 | **MRR_post:** 0.944  
**⬆️ 0 improved | ➡️ 8 same | ⬇️ 1 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 5 rag_not_called**

| Q | Diff | Category | User Question | Model Query | B.Pre | B.Post | B.Cos | M.Pre | M.Post | M.Cos | Δ Pre | Δ Post | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q21 | medium | multi_chunk | What happens to an employee's stock options both d… | TechCorp employee stock options during and after e… | 1 | 1 | 0.853 | 1 | 1 | 0.855 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q22 | medium | multi_chunk | What security-related obligations must a remote em… | security-related obligations remote employee worki… | 1 | 1 | 0.749 | 1 | 1 | 0.750 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q23 | medium | multi_chunk | What are the combined leave entitlements for an em… | combined leave entitlements for employee who is bo… | 2 | 1 | 0.685 | 1 | 2 | 0.690 | ⬆️ -1 | ⬇️ +1 | ⬇️ |
| Q24 | medium | inference | Can a TechCorp employee choose to work from a co-w… | TechCorp employee work from co-working space inste… | 3 | 1 | 0.812 | 3 | 1 | 0.811 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q25 | medium | inference | Is taking time off considered optional or essentia… | taking time off optional or essential at TechCorp | 1 | 1 | 0.862 | 1 | 1 | 0.864 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q26 | medium | inference | Does disclosing a conflict of interest mean an emp… | disclosing a conflict of interest wrongful employe… | 1 | 1 | 0.728 | 1 | 1 | 0.697 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q27 | medium | negation | In what situation is an employee not required to s… | situation when employee not required to submit doc… | 1 | 1 | 0.752 | 1 | 1 | 0.754 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q28 | medium | negation | What information will the IT team never ask an emp… | IT team never ask employee to provide information | 3 | 1 | 0.610 | 3 | 1 | 0.581 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q29 | medium | ambiguous | How much money does TechCorp allocate per employee… | TechCorp career-related growth allocation per empl… | 1 | 1 | 0.791 | 1 | 1 | 0.740 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q30 | medium | ambiguous | How often does TechCorp conduct its compensation-r… | *(RAG not called)* | — | — | — | — | — | — | — | — | rag_not_called |
| Q31 | hard | adversarial_paraphrase | Is there any official guarantee against punishment… | *(RAG not called)* | — | — | — | — | — | — | — | — | rag_not_called |
| Q32 | hard | adversarial_paraphrase | Above what spending level must an employee obtain … | *(RAG not called)* | — | — | — | — | — | — | — | — | rag_not_called |
| Q33 | hard | absent_plausible | What notice period or severance pay does TechCorp … | *(RAG not called)* | — | — | — | — | — | — | — | — | rag_not_called |
| Q34 | hard | absent_plausible | Does TechCorp offer an annual performance bonus or… | *(RAG not called)* | — | — | — | — | — | — | — | — | rag_not_called |
