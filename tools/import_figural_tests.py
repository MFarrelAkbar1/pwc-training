"""Build Logic subtest 10 ("Figural mix") from figural-tests.pdf.

The PDF has 3 pages and 16 questions:
    page 1     the 16 questions (no answers): one embedded JPEG per question under its number
    page 2     questions 1–11 again, with worked explanations and "Jawaban: x"
    page 3     questions 12–16 again (renumbered 1–5, "@belajarbro_id" watermark), with "Jawaban : X"
Topics (page 2 headings): 1–4 analogy, 5–7 odd one out, 8–11 series; 12–16 have no heading and are series.
All 16 go into one subtest, L10, in source order; each question keeps its source number ("Source no. N") and its
topic ("topic" in the JSON, shown in the results review).

The site images come from PAGE 1 ONLY (pages 2–3 carry the worked answers). Each embedded image is taken as is (no
page render, the PDF is only read): it already has the stimulus row on top and the options row below, at most five
cells a row, which is what import_figural_bank.py re-lays its strips into, so it only gets a white margin. The
watermarks on 12–16 are left in.

The key is read from the "Jawaban" lines on pages 2–3. It exists only once per question, so there is nothing to
cross-check it against (see REVIEW.md). "answer" is always that source key; it is also the scored answer, except for
the OVERRIDES (scored letter in "verifiedAnswer") and the AMBIGUOUS questions (not scored). Decisions from the review
live in the tables below (AMBIGUOUS, DISPUTED, OVERRIDES, EXPLANATIONS), so re-running the script keeps them. The blind answers are in
tools/figural_tests_blind_answers.txt. The timer is FIGURAL_TESTS_MINUTES in site/js/data.js.

Run:  python tools/import_figural_tests.py
"""
import io
import json
import re
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

from import_figural_bank import GAP, save_image

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "figural-tests.pdf"
DATA = ROOT / "site" / "data"
IMG = ROOT / "site" / "img"
TEST = 10
COUNT = 16

ANALOGY, ODD, SERIES = "analogy", "odd one out", "series"
TOPIC_OF = {n: ANALOGY for n in range(1, 5)} | {n: ODD for n in range(5, 8)} | {n: SERIES for n in range(8, 17)}
# Options printed in each picture: A–D on 12, 13, 15 and 16, A–E elsewhere.
LETTERS = {n: "ABCD" if n in (12, 13, 15, 16) else "ABCDE" for n in range(1, COUNT + 1)}
TEXT = {
    ANALOGY: "Figure 1 is to figure 2 as figure 3 is to ? The top row is the analogy; the bottom row is the options {r}.",
    ODD: "Which figure is the odd one out? (options {r})",
    SERIES: "Which option continues the series? The top row is the series; the bottom row is the options {r}.",
}

# ---------- review decisions (see REVIEW.md) ----------

# Not scored ("dropped", flag "ambiguous"); the source key stays in "answer". source no. -> note shown after answering.
AMBIGUOUS = {
    1: "Figure 1 → 2 keeps the dots and turns the lines 180° to the other side, so the answer is a two-line '>' on "
       "the left with the two dots on the right. No option shows that: A and C are the same drawing (a three-line "
       "arrow with two dots) and B has three dots.",
    4: "Each of the four tiles changes from figure 1 to 2 in a way that fits two rules: a 90° turn (top and bottom "
       "tiles one way, left and right tiles the other) or a flip across a diagonal. Applied to figure 3, the turn "
       "gives A and the flip gives B, and the example can't tell them apart.",
    11: "The steps alternate between swapping (and flipping) two opposite symbols and turning everything one place "
        "anticlockwise, and each step brings in one new symbol. Next the ↓ flips to ↑ at the top, the rectangle goes "
        "to the bottom and a new symbol appears on the right. A (S) and B (=) both do this; nothing decides which "
        "new symbol it is.",
    15: "The source's own key is hedged (\"probably B\"), and the pattern of crosses and circles (2, 1, 0, then 6 "
        "crosses) doesn't settle it: the blind check found B only with medium confidence.",
}

# The blind answer differs from the source key and the question is not ambiguous: keep the key, show a note.
DISPUTED = {}

# The site scores a different answer than the source key, by review decision: source no. -> (scored letter, note).
# The source key stays in "answer"; "verifiedAnswer" is the scored letter, answerSource and flag "recomputed".
OVERRIDES = {
    8: ("B", "Source key was D; this site scores B by review decision. Every symbol moves one side anticlockwise "
             "each step, and the black dot goes out, out, in, out, out, so next it is inside on the lower left: B. "
             "D puts the black dot at the upper right and the white circle outside on the lower left, which breaks "
             "the anticlockwise movement."),
}

# One-line explanation of the rule, only where I'm sure of it. Missing = empty explanation (listed in REVIEW.md).
EXPLANATIONS = {
    2: "Each shape is put inside a shape with one more side, touching at the top point: the triangle goes into a "
       "diamond, so the five-sided house goes into a hexagon with a point at the top.",
    3: "Figure 2 is figure 1 turned 180° (row order reversed, each row mirrored), so the answer is figure 3 turned "
       "180°.",
    5: "In every figure but C the number of leaves at the top equals the number of ovals at the bottom; C has 1 "
       "leaf and 2 ovals.",
    6: "The small arrowhead on the circle points clockwise in A–D and anticlockwise only in E.",
    12: "The stick keeps the same place in every option; the symbol on its end goes square, cross, triangle, circle, "
        "so next is the square again.",
    13: "The hourglasses go 4, 3, 2, 1 and the shoe shapes 0, 2, 4, 6, so next is no hourglass and 8 shoes.",
    14: "One more line from the centre each step (1, 2, 3, so 4) and the centre diamond alternates white and black, "
        "so next is a black diamond with 4 lines.",
}


# ---------- reading the PDF ----------

def page_images(page):
    """{question no.: xref} for page 1: each "N." heading is followed (same column, further down) by one image."""
    headings = [(b[0] > page.rect.width / 2, b[1], int(m.group(1))) for b in page.get_text("blocks")
                for m in re.finditer(r"(?:^|\n)\s*(\d+)\.", b[4])]
    images = {}
    for info in page.get_image_info(xrefs=True):
        x0, y0 = info["bbox"][:2]
        column = x0 > page.rect.width / 2
        above = [h for h in headings if h[0] == column and h[1] < y0]
        n = max(above, key=lambda h: h[1])[2]
        assert n not in images, f"question {n} has more than one image"
        images[n] = info["xref"]
    assert sorted(images) == list(range(1, COUNT + 1)), f"page 1 images for {sorted(images)}"
    return images


def column_text(page):
    """The page's text, left column first, then right column."""
    blocks = sorted(page.get_text("blocks"), key=lambda b: (b[0] > page.rect.width / 2, b[1]))
    return "\n".join(b[4] for b in blocks)


def read_key(doc):
    """{no.: letter} from the "Jawaban" lines: page 2 has 1–11, page 3 has 12–16 (numbered 1–5 there)."""
    answers = [a.upper() for i in (1, 2) for a in re.findall(r"Jawaban\s*:\s*([A-Ea-e])\b", column_text(doc[i]))]
    assert len(answers) == COUNT, f"found {len(answers)} keys, expected {COUNT}"
    key = dict(enumerate(answers, 1))
    bad = [n for n, a in key.items() if a not in LETTERS[n]]
    assert not bad, f"key is not one of the printed options for {bad}"
    return key


# ---------- images and JSON ----------

def write_images(doc):
    for n, xref in page_images(doc[0]).items():
        pic = Image.open(io.BytesIO(doc.extract_image(xref)["image"])).convert("RGB")
        out = Image.new("RGB", (pic.width + 2 * GAP, pic.height + 2 * GAP), "white")
        out.paste(pic, (GAP, GAP))
        save_image(out, IMG / f"figtests-{n:02}.png")


def build_test(key):
    questions = []
    for n in range(1, COUNT + 1):
        topic, letters = TOPIC_OF[n], LETTERS[n]
        q = {
            "id": f"L{TEST}-Q{n:02}",
            "text": TEXT[topic].format(r=f"{letters[0]}–{letters[-1]}"),
            "image": f"img/figtests-{n:02}.png",
            "imageAlt": f"Source question {n} ({topic}), with the answer options {letters[0]}–{letters[-1]} drawn "
                        "in the picture.",
            "sourceRef": f"Source no. {n}",
            "topic": topic,
            "options": {letter: f"Figure {letter}" for letter in letters},
            "answer": key[n],
        }
        if n in AMBIGUOUS:
            q["verifiedAnswer"] = None
            q["answerSource"] = "dropped"
        elif n in OVERRIDES:
            q["verifiedAnswer"] = OVERRIDES[n][0]
            q["answerSource"] = "recomputed"
        q["explanation"] = EXPLANATIONS.get(n, "")
        q["source"] = "imported"
        if n in AMBIGUOUS:
            q["flag"] = {"type": "ambiguous", "note": AMBIGUOUS[n]}
        elif n in OVERRIDES:
            q["flag"] = {"type": "recomputed", "note": OVERRIDES[n][1]}
        elif n in DISPUTED:
            q["flag"] = {"type": "disputed", "note": DISPUTED[n]}
        questions.append(q)
    return {"id": f"L{TEST}", "section": "logic", "test": TEST, "title": "Logic – Figural mix (imported)",
            "source": "imported", "questions": questions}


def main():
    doc = fitz.open(PDF)
    key = read_key(doc)
    write_images(doc)
    out = DATA / f"logic-{TEST}.json"
    out.write_text(json.dumps(build_test(key), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    scored = COUNT - len(AMBIGUOUS)
    print(f"wrote {out.relative_to(ROOT)}: source no. 1–{COUNT} ({scored} scored, {len(AMBIGUOUS)} dropped, "
          f"{len(OVERRIDES)} overridden, {len(DISPUTED)} disputed); key: one copy only (pages 2–3), no cross-check "
          "possible")


if __name__ == "__main__":
    main()
