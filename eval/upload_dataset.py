"""
Upload the 18-question tool-routing eval dataset to LangSmith.

Run from project root:
    .venv\Scripts\python eval/upload_dataset.py
"""

import os
import sys


def _load_env() -> None:
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


_load_env()

from langsmith import Client  # noqa: E402

DATASET_NAME = "tool-routing-eval-v1"

EXAMPLES = [
    # ── calculator (4) ────────────────────────────────────────────────────
    {
        "question": "What is 1250 multiplied by 0.18?",
        "expected_tool": "calculator",
        "expected_answer": "225",
    },
    {
        "question": "What is (500 + 300) * 0.20?",
        "expected_tool": "calculator",
        "expected_answer": "160",
    },
    {
        "question": "What is 25% of 348?",
        "expected_tool": "calculator",
        "expected_answer": "87",
    },
    {
        "question": "What is 9750 divided by 13?",
        "expected_tool": "calculator",
        "expected_answer": "750",
    },
    # ── web_search (6) ────────────────────────────────────────────────────
    {
        "question": "What is the weather in Istanbul today?",
        "expected_tool": "web_search",
        "expected_answer": "current temperature and conditions",
    },
    {
        "question": "What is the current EUR to TRY exchange rate?",
        "expected_tool": "web_search",
        "expected_answer": "current rate",
    },
    {
        "question": "What are the latest developments in AI this week?",
        "expected_tool": "web_search",
        "expected_answer": "recent news",
    },
    {
        "question": "Who is the current president of the United States?",
        "expected_tool": "web_search",
        "expected_answer": "current president name",
    },
    {
        "question": "What is the current population of Turkey?",
        "expected_tool": "web_search",
        "expected_answer": "current population figure",
    },
    {
        "question": "What is the average temperature in Istanbul?",
        "expected_tool": "web_search",
        "expected_answer": "current seasonal data",
    },
    # ── rag (3) ───────────────────────────────────────────────────────────
    {
        "question": "Search my documents for the return policy.",
        "expected_tool": "rag",
        "expected_answer": "relevant chunk from docs",
    },
    {
        "question": "What does my document say about payment terms?",
        "expected_tool": "rag",
        "expected_answer": "relevant chunk from docs",
    },
    {
        "question": "Find information about delivery time in my files.",
        "expected_tool": "rag",
        "expected_answer": "relevant chunk from docs",
    },
    # ── none (4) ──────────────────────────────────────────────────────────
    {
        "question": "Who wrote Hamlet?",
        "expected_tool": "none",
        "expected_answer": "Shakespeare",
    },
    {
        "question": "What is the capital of France?",
        "expected_tool": "none",
        "expected_answer": "Paris",
    },
    {
        "question": "What is the chemical formula of water?",
        "expected_tool": "none",
        "expected_answer": "H2O",
    },
    {
        "question": "In what year did World War II end?",
        "expected_tool": "none",
        "expected_answer": "1945",
    },
    # ── edge cases (1) ────────────────────────────────────────────────────
    {
        "question": "Find the population of Turkey in my documents.",
        "expected_tool": "web_search",
        "expected_answer": "no documents exist — should fall back to web",
    },
]


def main() -> None:
    client = Client()

    existing = list(client.list_datasets(dataset_name=DATASET_NAME))
    if existing:
        print(f"Dataset '{DATASET_NAME}' already exists (id={existing[0].id}).")
        print("To re-upload: delete it on smith.langchain.com first, then re-run.")
        sys.exit(0)

    print(f"Creating dataset '{DATASET_NAME}'...")
    dataset = client.create_dataset(
        DATASET_NAME,
        description=(
            "Tool routing eval: 18 questions — "
            "calculator (4), web_search (6), rag (3), none (4), edge case (1)."
        ),
    )

    for ex in EXAMPLES:
        client.create_example(
            inputs={"question": ex["question"]},
            outputs={
                "expected_tool": ex["expected_tool"],
                "expected_answer": ex["expected_answer"],
            },
            dataset_id=dataset.id,
        )
        print(f"  + [{ex['expected_tool']:<10}]  {ex['question'][:65]}")

    print(f"\n{len(EXAMPLES)} examples uploaded.")
    print("View: https://smith.langchain.com > Datasets > tool-routing-eval-v1")


if __name__ == "__main__":
    main()
