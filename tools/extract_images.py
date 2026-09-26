"""Crop every chart/table out of the numerical section (pages 1-62).

Each PDF page is one scanned image with a hidden text layer, so charts are not
separate images. Every chart sits between a "Study the ... below it." line and
the next "Question N" line, so we use those text positions to crop it.

When "Study the ..." is at the bottom of a page, the chart is often on the next
page instead; if the crop comes out blank we take the top of the next page.

Output: site/img/p<page>.png, named after the page the chart is actually on
(a page never has more than one chart).
"""
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "dlstudocu.com_pwc-aptitude-test-past-questions-and-solutions.pdf"
OUT = ROOT / "site" / "img"
LAST_NUMERICAL_PAGE = 62
OVERLAP = 30  # the chart's bottom edge runs slightly past the "Question N" label
ZOOM = 2      # render at 144 dpi so the numbers stay readable
PAGE_TOP = 40  # skip the page header area when a chart starts on a new page


def first_question_top(blocks):
    below = [b for b in blocks if "Question" in b[4]]
    return below[0][1] + OVERLAP if below else None


def chart_box(page):
    """Return the crop rectangle below "Study the ..." on this page, or None."""
    blocks = sorted(page.get_text("blocks"), key=lambda b: b[1])
    for i, b in enumerate(blocks):
        if b[4].strip().startswith("Study the"):
            bottom = first_question_top(blocks[i + 1:]) or page.rect.height - 60
            return fitz.Rect(55, b[3] + 2, 560, bottom)
    return None


def next_page_box(page):
    """The chart continues at the top of this page, down to its first question."""
    blocks = sorted(page.get_text("blocks"), key=lambda b: b[1])
    bottom = first_question_top(blocks) or page.rect.height - 60
    return fitz.Rect(55, PAGE_TOP, 560, bottom)


def is_blank(pix):
    """True if (almost) every pixel is white-ish."""
    samples = pix.samples
    step = pix.n * 7  # sample every 7th pixel; plenty for this check
    dark = sum(1 for i in range(0, len(samples), step) if samples[i] < 200)
    return dark < len(samples) / step * 0.005


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("p*.png"):
        old.unlink()
    doc = fitz.open(PDF)
    matrix = fitz.Matrix(ZOOM, ZOOM)
    for page_no in range(1, LAST_NUMERICAL_PAGE + 1):
        page = doc[page_no - 1]
        box = chart_box(page)
        if box is None:
            continue
        pix = page.get_pixmap(matrix=matrix, clip=box)
        chart_page = page_no
        if is_blank(pix):
            chart_page = page_no + 1
            box = next_page_box(doc[chart_page - 1])
            pix = doc[chart_page - 1].get_pixmap(matrix=matrix, clip=box)
        name = f"p{chart_page:02d}.png"
        pix.save(OUT / name)
        moved = f"  (chart on next page, 'Study' on p{page_no})" if chart_page != page_no else ""
        print(f"{name}  y {box.y0:.0f}-{box.y1:.0f}{moved}")


if __name__ == "__main__":
    main()
