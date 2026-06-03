"""
PDF chunking test script.

Usage:
    .venv\Scripts\python scripts\test_pdf_chunking.py <path-to-pdf>

Runs extract_pages() + chunk_document() locally (no DB, no embeddings).
Prints chunk stats and content so you can verify chunking quality.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Make sure the project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.pdf_extractor import extract_pages, PDFExtractionError
from app.services.chunking import chunk_document


def run(pdf_path: str) -> None:
    path = Path(pdf_path)
    if not path.exists():
        print(f"ERROR: File not found: {pdf_path}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"PDF: {path.name}")
    print(f"{'='*60}\n")

    # --- Step 1: extract pages ---
    content = path.read_bytes()
    try:
        pages = extract_pages(content)
    except PDFExtractionError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print(f"Pages extracted: {len(pages)}")
    total_chars = sum(len(p["text"]) for p in pages)
    print(f"Total chars: {total_chars}\n")

    # Show first page raw text (truncated)
    # Show detected heading levels
    import fitz as _fitz
    from app.services.pdf_extractor import _build_heading_level_map
    _doc = _fitz.open(stream=content, filetype="pdf")
    _level_map = _build_heading_level_map(_doc)
    if _level_map:
        print("Detected heading levels:")
        for size, marker in sorted(_level_map.items(), reverse=True):
            print(f"  {size:.1f}pt → {marker.strip()}")
    else:
        print("No heading levels detected.")
    print()

    print("--- Page 1 raw text (first 800 chars) ---")
    print(pages[0]["text"][:800])
    print("...\n")

    # --- Step 2: merge pages ---
    merged_text = "\n\n".join(p["text"] for p in pages)

    # --- Step 3: chunk ---
    chunks = chunk_document(merged_text, source_filename=path.name)

    print(f"{'='*60}")
    print(f"Chunks produced: {len(chunks)}")
    print(f"{'='*60}\n")

    # Token distribution
    sizes = [c.token_count for c in chunks]
    buckets = {
        "< 20 tokens":   sum(1 for s in sizes if s < 20),
        "20–99 tokens":  sum(1 for s in sizes if 20 <= s < 100),
        "100–299 tokens": sum(1 for s in sizes if 100 <= s < 300),
        "300+ tokens":   sum(1 for s in sizes if s >= 300),
    }
    print("Token distribution:")
    for label, count in buckets.items():
        pct = count / len(chunks) * 100 if chunks else 0
        print(f"  {label:20s}: {count:3d}  ({pct:.0f}%)")
    avg = sum(sizes) / len(sizes) if sizes else 0
    print(f"  {'Average':20s}: {avg:.1f} tokens")
    print()

    # All chunks
    print(f"{'='*60}")
    print("All chunks:")
    print(f"{'='*60}\n")
    for i, chunk in enumerate(chunks):
        heading = f" [section: {chunk.section_heading}]" if chunk.section_heading else ""
        print(f"[{i:03d}] {chunk.token_count:4d} tokens{heading}")
        # Show first 200 chars of content
        preview = chunk.text.replace("\n", "\\n")
        if len(preview) > 200:
            preview = preview[:200] + "..."
        print(f"      {preview}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: .venv\\Scripts\\python scripts\\test_pdf_chunking.py <path-to-pdf>")
        sys.exit(1)
    run(sys.argv[1])
