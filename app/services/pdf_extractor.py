from __future__ import annotations

import re
from collections import Counter

import fitz  # pymupdf

# Lines longer than this are never treated as headings (e.g. full-width table rows).
_MAX_HEADING_CHARS: int = 200
# Minimum ratio above body size for a font to be a heading candidate.
_HEADING_MIN_RATIO: float = 1.10
# Page-number artifacts: bare digits ("1") or digits with trailing punctuation ("5.", "5)")
_PAGE_NUMBER_RE = re.compile(r"^\d+[.)]*$")


class PDFExtractionError(ValueError):
    """Raised when PDF cannot be parsed or yields no text."""


def _build_heading_level_map(doc) -> dict[float, str]:
    """
    Two-pass scan: collect all span font sizes across the entire document,
    determine the body size (most frequent), then map the top ≤3 larger
    unique sizes to H1/H2/H3 markers.

    Returns {rounded_size: markdown_prefix} e.g. {18.0: "# ", 14.0: "## "}.
    Sizes within 0.5pt of each other are treated as the same level.
    """
    size_counter: Counter = Counter()
    for page in doc:
        raw = page.get_text("dict")
        for block in raw.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    size = span.get("size", 0.0)
                    if text and size > 0:
                        size_counter[round(size, 1)] += 1

    if not size_counter:
        return {}

    body_size: float = size_counter.most_common(1)[0][0]
    min_heading_size: float = body_size * _HEADING_MIN_RATIO

    # Collect unique sizes above the heading threshold, largest first.
    raw_heading_sizes = sorted(
        {s for s in size_counter if s >= min_heading_size},
        reverse=True,
    )

    # Cluster sizes within 0.5pt so minor rendering differences don't
    # produce spurious extra levels (e.g. 18.0 and 18.1 → same level).
    clusters: list[float] = []
    for size in raw_heading_sizes:
        if not clusters or clusters[-1] - size > 0.5:
            clusters.append(size)

    markers = ["# ", "## ", "### "]
    level_map: dict[float, str] = {}
    for i, cluster_size in enumerate(clusters[:3]):
        # All raw sizes within 0.5pt of this cluster get the same marker.
        for size in raw_heading_sizes:
            if abs(size - cluster_size) <= 0.5 and size not in level_map:
                level_map[size] = markers[i]

    return level_map


def _page_to_text_with_headings(page, level_map: dict[float, str]) -> str:
    """
    Reconstruct page text from get_text("dict") blocks.

    Uses the document-level level_map to assign # / ## / ### markers to
    lines whose maximum span font size falls in a heading cluster.
    Falls back to plain get_text("text") when no font-size data is available.
    """
    raw = page.get_text("dict")
    blocks = [b for b in raw.get("blocks", []) if b.get("type") == 0]

    if not blocks:
        return page.get_text("text")

    # Pre-sort level_map thresholds descending for fast lookup.
    sorted_thresholds = sorted(level_map.keys(), reverse=True)

    output_blocks: list[str] = []
    for block in blocks:
        block_lines: list[str] = []
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            line_text = "".join(s.get("text", "") for s in spans)
            stripped = line_text.strip()
            if not stripped:
                continue

            max_size = round(
                max(
                    (s.get("size", 0.0) for s in spans if s.get("text", "").strip()),
                    default=0.0,
                ),
                1,
            )

            prefix = ""
            if len(stripped) <= _MAX_HEADING_CHARS:
                for threshold in sorted_thresholds:
                    if max_size >= threshold:
                        prefix = level_map[threshold]
                        break

            block_lines.append(f"{prefix}{stripped}" if prefix else line_text)

        if block_lines:
            output_blocks.append("\n".join(block_lines))

    # Drop noise blocks: empty, page-number artifacts ("1", "5.", "5)"), or
    # purely decorative symbols with no alphanumeric content (lone bullets etc.)
    output_blocks = [
        b for b in output_blocks
        if b.strip()
        and not _PAGE_NUMBER_RE.match(b.strip())
        and any(c.isalnum() for c in b)
    ]
    return "\n\n".join(output_blocks)


def extract_pages(content: bytes) -> list[dict]:
    """
    Reads PDF bytes, returns list of {page: int, text: str} per page.

    Heading levels (# / ## / ###) are assigned based on relative font sizes
    across the entire document — the largest heading fonts become H1, the
    next level H2, and so on (up to H3). This preserves document hierarchy
    in the chunk metadata instead of flattening everything to H1.

    Raises PDFExtractionError if no text is found across all pages.
    """
    doc = fitz.open(stream=content, filetype="pdf")
    level_map = _build_heading_level_map(doc)

    pages = []
    for page_num, page in enumerate(doc, start=1):
        text = _page_to_text_with_headings(page, level_map)
        # Strip lines that consist only of page-number artifacts ("1", "5.", "42)").
        text = re.sub(r"(?m)^[ \t]*\d+[.)]*[ \t]*$", "", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if text.strip():
            pages.append({"page": page_num, "text": text.strip()})

    if not pages:
        raise PDFExtractionError(
            "No extractable text found. PDF may be image-only (scanned). "
            "OCR is not supported yet."
        )
    return pages
