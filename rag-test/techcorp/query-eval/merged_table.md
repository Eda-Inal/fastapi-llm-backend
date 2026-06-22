# TechCorp — Query Quality Eval (Merged per Model)

One section per model. Same-model runs are merged (latest run wins on duplicate questions).

*Generated: 2026-06-22 17:26*


## llama-3.3-70b-versatile
**Runs merged:** run_010, run_011  
**Questions:** 34/34  
**recall@5:** 1.0 | **MRR_pre:** 0.937 | **MRR_post:** 0.983  
**⬆️ 0 improved | ➡️ 28 same | ⬇️ 1 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 5 rag_not_called**

> **⚠️ Q30–Q34: `rag_not_called` due to Groq TPD rate limit (HTTP 429), not a model decision. Re-run needed.**
>
> **⬇️ Q23 (multi_chunk)** — Same pattern seen in all three models: dense rank improved (2→1) but reranker degraded (1→2). The model query focuses on one aspect of the combined leave policy, causing the reranker to prefer a different chunk over the primary one.

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

## meta-llama/llama-4-scout-17b-16e-instruct
**Runs merged:** run_001, run_002, run_003, run_004  
**Questions:** 34/34  
**recall@5:** 1.0 | **MRR_pre:** 0.913 | **MRR_post:** 0.968  
**⬆️ 1 improved | ➡️ 29 same | ⬇️ 3 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 1 rag_not_called**

> **⬆️ Q31 (adversarial_paraphrase)** — Scout reworded the paraphrase into its semantic core and helped the reranker push the correct chunk from rank 2 to rank 1. The only model that actively improved a hard question.
>
> **⬇️ Q23 (multi_chunk)** — Dense improved (2→1) but reranker degraded (1→2). Consistent cross-model failure point.
>
> **⬇️ Q30 (ambiguous)** — Scout compressed the question to a terse keyword phrase; reranker preferred the original sentence form. Rank slipped 1→2 after reranking.
>
> **⬇️ Q34 (absent_plausible)** — Model query raised the dense top-1 score (+0.048), increasing false-positive retrieval risk for a question that has no answer in the knowledge base.
>
> **⏭️ Q26 (inference)** — Scout answered the conflict-of-interest ethics question from its own knowledge without invoking RAG.

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

## openai/gpt-oss-120b
**Runs merged:** run_005, run_007, run_008, run_009  
**Questions:** 34/34  
**recall@5:** 1.0 | **MRR_pre:** 0.9 | **MRR_post:** 1.0  
**⬆️ 2 improved | ➡️ 31 same | ⬇️ 1 worse | 🔴 0 regression | 🟢 0 recovered | ⏭️ 0 rag_not_called**

> **✅ RAG called on every question** — GPT-oss is the only model with 0 `rag_not_called`. It consistently invokes retrieval even on hard, ambiguous, and absent-answer questions.
>
> **⬆️ Q31 (adversarial_paraphrase)** — Identical improvement to Scout: reranker rank 2→1. All models that called RAG on Q31 achieved this improvement, confirming the retrieval pipeline handles it well once the semantic core is passed.
>
> **⬆️ Q33 (absent_plausible)** — GPT-oss reduced both the dense top-1 score (0.836→0.794) and rerank score (0.882→0.803). Lower scores on an absent-answer question mean fewer false-positive retrieval hits — a positive result. No other model achieved this.
>
> **⬇️ Q34 (absent_plausible)** — Dense top-1 slightly increased (+0.041, bad), but rerank score dropped dramatically (0.559→0.306), which is actually beneficial. The verdict is ⬇️ due to the dense signal, but the reranker behaviour is arguably the better signal here.
>
> **MRR_post = 1.0** — Every question where the correct chunk exists, GPT-oss placed it at rank 1 after reranking. Strongest post-rerank performance of the three models.

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
| Q31 | hard | adversarial_paraphrase | Is there any official guarantee against punishment… | official guarantee against punishment for staff me… | 1 | 2 | 0.611 | 1 | 1 | 0.607 | ➡️ 0 | ⬆️ -1 | ⬆️ |
| Q32 | hard | adversarial_paraphrase | Above what spending level must an employee obtain … | Above what spending level must an employee obtain … | 8 | 1 | 0.633 | 8 | 1 | 0.633 | ➡️ 0 | ➡️ 0 | ➡️ |
| Q33 | hard | absent_plausible | What notice period or severance pay does TechCorp … | notice period severance pay TechCorp let employee … | 0.836 | 0.882 | — | 0.794 | 0.803 | — | ⬆️ -0.043 | ⬆️ -0.079 | ⬆️ |
| Q34 | hard | absent_plausible | Does TechCorp offer an annual performance bonus or… | TechCorp annual performance bonus variable pay amo… | 0.706 | 0.559 | — | 0.747 | 0.306 | — | ⬇️ +0.041 | ⬆️ -0.253 | ⬇️ |
