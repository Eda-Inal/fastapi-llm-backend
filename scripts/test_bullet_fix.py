"""
Tests the bullet-list chunking fix directly against the known problematic pattern.

ironstack_guide.pdf style: each bullet is a separate PDF block, so pdf_extractor
joins them with "\n\n" (double newline). Before the fix, _extract_list_segments
would close the list on every blank line, producing one tiny chunk per bullet.

Run: .venv\Scripts\python scripts\test_bullet_fix.py
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.chunking import chunk_document

# This is exactly what pdf_extractor.py produces when each bullet is a separate
# PDF block — the same pattern that caused fragmentation in ironstack_guide.pdf.
IRONSTACK_STYLE_TEXT = """\
# SECTION 1: PROGRAMMING LANGUAGE COMPARISON

Four languages are evaluated: Python, Go, Rust, and Node.js.

| Language | Perf Score | Dev Speed |
|----------|------------|-----------|
| Python   | 4/10       | 10/10     |
| Rust     | 10/10      | 4/10      |
| Go       | 8/10       | 8/10      |
| Node.js  | 7/10       | 8/10      |

Key Findings:

- Python scores lowest on raw performance (4/10) but highest on developer speed (10/10).

- Rust achieves a perfect performance score (10/10) but has the steepest learning curve.

- Node.js is the go-to for I/O-bound workloads.

- Go balances performance and developer speed well, making it a strong general-purpose choice.

# SECTION 2: DEPLOYMENT OPTIONS

Podman:

- Daemonless container engine, does not require root privileges.

- Compatible with Docker CLI syntax.

- Preferred for security-sensitive environments.

In this document:

- All benchmarks were run on identical hardware configurations.

- Results represent averages across 10 test runs.

Recommendations by use case:

- High performance: Rust

- Rapid prototyping: Python

- Balanced workloads: Go

- I/O-heavy services: Node.js
"""


def run() -> None:
    chunks = chunk_document(IRONSTACK_STYLE_TEXT, source_filename="ironstack_style_test")

    print(f"\n{'='*60}")
    print("Bullet Fix Verification Test")
    print(f"Input has bullets separated by \\n\\n (separate PDF blocks)")
    print(f"{'='*60}\n")
    print(f"Chunks produced: {len(chunks)}\n")

    bullet_chunks = [c for c in chunks if c.text.strip().startswith("-")]
    list_block_chunks = [c for c in chunks if "\n-" in c.text or c.text.strip().startswith("-")]

    for i, chunk in enumerate(chunks):
        heading = f" [section: {chunk.section_heading}]" if chunk.section_heading else ""
        preview = chunk.text.replace("\n", "\\n")
        if len(preview) > 150:
            preview = preview[:150] + "..."
        print(f"[{i:02d}] {chunk.token_count:4d} tok{heading}")
        print(f"      {preview}\n")

    print(f"{'='*60}")
    print("VERDICT")
    print(f"{'='*60}")

    # Check: are the "Key Findings" bullets in a single chunk?
    key_findings_chunks = [
        c for c in chunks
        if "Python scores" in c.text or "Rust achieves" in c.text or "Node.js is" in c.text
    ]
    bullets_in_one = len(key_findings_chunks) == 1
    print(f"  'Key Findings' bullets in 1 chunk : {'✓ YES' if bullets_in_one else '✗ NO (still fragmented)'}")

    podman_chunks = [c for c in chunks if "Daemonless" in c.text or "Docker CLI" in c.text]
    podman_in_one = len(podman_chunks) == 1
    print(f"  'Podman' bullets in 1 chunk       : {'✓ YES' if podman_in_one else '✗ NO (still fragmented)'}")

    rec_chunks = [c for c in chunks if "High performance" in c.text or "Rapid prototyping" in c.text]
    rec_in_one = len(rec_chunks) == 1
    print(f"  'Recommendations' bullets in 1 chunk: {'✓ YES' if rec_in_one else '✗ NO (still fragmented)'}")

    all_pass = bullets_in_one and podman_in_one and rec_in_one
    print(f"\n  Overall: {'ALL PASS ✓' if all_pass else 'FAIL ✗'}")


if __name__ == "__main__":
    run()
