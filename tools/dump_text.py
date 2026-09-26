"""Dump the text of every PDF page to tools/out/page-NN.txt.

The PDF's text order is scrambled (question stems often come after the options),
so these files are only a first draft to copy from while building the JSON by hand.
"""
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "dlstudocu.com_pwc-aptitude-test-past-questions-and-solutions.pdf"
OUT = Path(__file__).resolve().parent / "out"


def main():
    OUT.mkdir(exist_ok=True)
    doc = fitz.open(PDF)
    for i, page in enumerate(doc, start=1):
        (OUT / f"page-{i:02d}.txt").write_text(page.get_text(), encoding="utf-8")
    print(f"Wrote {len(doc)} pages to {OUT}")


if __name__ == "__main__":
    main()
