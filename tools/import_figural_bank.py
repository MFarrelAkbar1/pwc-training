"""Build Logic subtests 6–9 from the figural question bank PDF ([4]Bank_Soal_Psikotes_Figural_Spasial.pdf).

The PDF has 250 questions in 10 topics of 25. Only four topics are imported, and only their "sedang" (medium) and
"sulit" (hard) questions, 17 per topic:
    L6  Analogi Figural                     no. 1–25
    L7  Klasifikasi & Pengelompokan Bentuk  no. 26–50
    L8  Seri/Pola Figural                   no. 51–75
    L9  Matriks Figural                     no. 226–250

Each question in the PDF is one embedded image: a single strip of framed cells (stimulus cells, then options A–D).
The script takes that embedded image as is (no page render, the PDF is only read) and re-lays the cells out on
a grid, stimulus rows first, then the four options, so the picture stays readable at phone width. The
classification topic's first cell only says "Cari 1 gambar yang berbeda" (find the odd one out); it is left out
because the question text says the same in English.

The key is read from section B (blueprint table) and cross-checked with section D (key summary); the script stops
if the two disagree for an imported question. "answer" is always that source key. Decisions from the review live
in the tables below (AMBIGUOUS, DISPUTED, EXPLANATIONS), so re-running the script keeps them. Details: REVIEW.md.
The timer is not in the JSON: it is SECTIONS.logic.testMinutes in site/js/data.js.

Run:  python tools/import_figural_bank.py
"""
import io
import json
import re
from pathlib import Path

import fitz  # PyMuPDF
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "[4]Bank_Soal_Psikotes_Figural_Spasial.pdf"
DATA = ROOT / "site" / "data"
IMG = ROOT / "site" / "img"
LEVELS = ("sedang", "sulit")  # imported difficulties; "mudah" is skipped
GAP = 24  # pixels between cells in the re-laid image
OPTIONS = ["A", "B", "C", "D"]

# test number -> (first, last bank number, topic name as in the PDF, title, question text, stimulus layout)
# layout: how many stimulus cells go on each row before the options row.
TOPICS = {
    6: (1, 25, "Analogi Figural", "Figural analogies",
        "A is to B as C is to ? The top row is the analogy (A : B = C : ?); the bottom row is the options A–D.",
        [4]),
    7: (26, 50, "Klasifikasi & Pengelompokan Bentuk", "Odd one out",
        "Three of the four figures share a rule; one does not. Which figure is the odd one out?",
        []),
    8: (51, 75, "Seri/Pola Figural", "Figural series",
        "Figures 1–4 form a series. Which option is figure 5? The top row is the series; the bottom row is the options A–D.",
        [5]),
    9: (226, 250, "Matriks Figural & Penalaran Visual Kompleks", "Figural matrices",
        "Each row and column of the 3×3 matrix follows a rule (shape, rotation and/or shading). Which option fills "
        "the cell marked ?  The grid is on top; the bottom row is the options A–D.",
        [3, 3, 3]),
}

# ---------- review decisions (see REVIEW.md) ----------

# Two or more options satisfy the rule (or look the same): not scored ("dropped", flag "ambiguous").
# bank no. -> note shown after answering. The source key stays in "answer".
_TURN_HIDDEN = ("The example changes a square only by the {fill}; turning a square 90° shows nothing, so you can't "
                "tell whether it was turned too. The star with the {fill} is {a} if it wasn't turned and {b} if it was: "
                "both fit.")
_SAME = "The rule gives {what}, but options {a} and {b} are the same drawing (only the hatch lines' position differs)."
_SAME_EXACT = "The rule gives {what}, but options {a} and {b} are the same drawing."
_ODD_TWO = "Two rules single out different figures: {first}; {second}."
AMBIGUOUS = {
    11: _TURN_HIDDEN.format(fill="cross-hatching", a="B", b="C"),
    21: _TURN_HIDDEN.format(fill="dots", a="A", b="B"),
    33: _ODD_TWO.format(first="A is the only shaded figure",
                        second="D is the only one with an odd number of sides (square 4, hexagons 6, pentagon 5)"),
    34: _ODD_TWO.format(first="A is the only one with an odd number of sides (triangle; hexagon 6, star 10)",
                        second="B is the only curved figure"),
    39: _ODD_TWO.format(first="C is the only one with an odd number of sides and the only one pointing down",
                        second="B is the only curved figure"),
    40: _ODD_TWO.format(first="A is the only tilted figure (and the only odd-sided one)",
                        second="D is the only curved figure"),
    45: _ODD_TWO.format(first="B is the only tilted figure", second="C is the only curved figure (A and D are the same star)"),
    50: _ODD_TWO.format(first="A is the only one with an odd number of sides (B and C are the same square)",
                        second="D is the only curved figure"),
    51: _SAME.format(what="a hatched circle (fill cycles none, hatched, cross-hatched)", a="A", b="D"),
    52: _SAME_EXACT.format(what="the square turned like figure 2 (it turns 30° a step and repeats every 90°)", a="B", b="C"),
    54: _SAME_EXACT.format(what="the square turned like figure 2 (it turns 30° a step and repeats every 90°)", a="A", b="B"),
    55: _SAME.format(what="two hatched circles (the cycle one plain, two hatched, three cross-hatched repeats)", a="C", b="D"),
    56: _SAME.format(what="two hatched hexagons (the cycle one plain, two hatched, three cross-hatched repeats)", a="A", b="B"),
    57: _SAME.format(what="two hatched crosses (the cycle one plain, two hatched, three cross-hatched repeats)", a="B", b="C"),
    59: _SAME_EXACT.format(what="an arrow bigger than figure 4", a="C", b="D"),
    60: _SAME.format(what="a hatched pentagon (fill cycles none, hatched, cross-hatched)", a="A", b="B"),
    61: _SAME.format(what="a hatched star (fill cycles none, hatched, cross-hatched)", a="B", b="D"),
    64: _SAME.format(what="a hatched square (fill cycles none, hatched, cross-hatched)", a="A", b="D"),
    70: _SAME_EXACT.format(what="an arrow bigger than figure 4", a="A", b="B"),
    71: "The count goes 1, 2, 3, 4, so figure 5 should have 5 diamonds, but no option has 5. "
        "B, C and D are the same four diamonds.",
    229: _SAME.format(what="a hatched diamond (turning a diamond shows nothing)", a="A", b="C"),
    231: _SAME.format(what="a medium hatched circle", a="B", b="C"),
    236: _SAME.format(what="a medium hatched diamond", a="A", b="B"),
    238: _SAME.format(what="a hatched cross (turning a cross by 90° or 180° shows nothing)", a="A", b="C"),
    246: _SAME.format(what="a hatched diamond (turning a diamond shows nothing)", a="A", b="D"),
}

# My blind answer differs from the source key and the question is not ambiguous: keep the key, show a note.
# (None after the review: every scored question matched.)
DISPUTED = {}

# One-line explanation of the rule, only where I'm sure of it. Missing = empty explanation (listed in REVIEW.md).
_MATRIX = ("Each row keeps one shape; across a row it turns 90° a step and the fill goes through plain, hatched and "
           "cross-hatched in a shifted order, so the missing cell is {answer}.")
_MATRIX_SIZE = ("Each row keeps one shape; size (small, medium, large), fill (plain, hatched, cross-hatched) and a 90° "
                "turn per column rotate through the rows, so the missing cell is {answer}.")
EXPLANATIONS = {
    5: "The plus turns 45° into an X and gets a grey dotted fill; a turned circle looks the same, so the answer is a "
       "grey dotted circle.",
    7: "The shape becomes three smaller copies turned 45°, so the pentagon becomes three small turned pentagons.",
    9: "The shape becomes three smaller turned copies; a turned circle looks the same, so the answer is three small "
       "circles.",
    10: "The shape turns 180° and gets a grey fill, so the triangle becomes a grey triangle pointing down.",
    13: "The shape gets bigger and grey, so the answer is a big grey hexagon.",
    14: "The shape turns 90° and gets hatched; a diamond turned 90° looks the same, so the answer is a hatched diamond.",
    15: "The shape becomes two smaller copies, so the circle becomes two small circles.",
    16: "The shape gets bigger and grey, so the answer is a big grey square (B and C are the same, both too small).",
    17: "The shape turns 180° and gets a grey fill; a cross turned 180° looks the same, so the answer is a grey cross "
        "of the same size (A is too big).",
    18: "The shape is flipped upside down, made bigger and hatched; a flipped square looks the same, so the answer is a "
        "big hatched square (A is not bigger).",
    19: "The shape gets bigger and grey, so the answer is a big grey square (A and B are the same, both too small).",
    20: "The shape turns 180° and gets cross-hatched, so the answer is a cross-hatched triangle pointing down (A is not "
        "turned).",
    22: "The shape turns 180° and gets a grey fill; a turned circle looks the same, so the answer is a grey circle.",
    24: "The shape turns a little and gets a grey cross-hatched fill, so the answer is the turned grey cross-hatched star.",
    28: "Three figures have two shapes; A has only one.",
    29: "Three figures have two shapes; A has only one.",
    31: "Three figures are shaded (dots, cross-hatch, hatch); D is empty.",
    35: "Three figures have two shapes; C has only one.",
    37: "Three figures are the same pair of circles; A is a single star.",
    41: "Three figures are the same star; A is a triangle.",
    42: "D is the only tilted figure (B and C are the same upright hexagon, A is an upright star).",
    43: "Three figures are filled grey; D is empty.",
    44: "Three figures have two shapes; B has only one.",
    47: "Three figures have two shapes; C has only one.",
    49: "Three figures are filled grey; A is empty.",
    53: "The arrow turns 30° anticlockwise and gets bigger each step (0°, 30°, 60°, 90°), so next is a bigger arrow at "
        "120°, pointing up-left.",
    62: "The star turns 45° each step (0°, 45°, 90°, 135°), so next it is turned 180°, one point straight down.",
    68: "The circle's diameter grows by the same amount each step, so next is the circle one step bigger than figure 4 "
        "(D; C is bigger still).",
    72: "The circle's diameter grows by the same amount each step, so next is the circle one step bigger than figure 4 "
        "(A; B is bigger still).",
    73: "The pentagon gets bigger and turns 45° each step (0°, 45°, 90°, 135°), so next is a bigger pentagon turned "
        "180°, point down.",
    227: _MATRIX.format(answer="a hatched pentagon turned 180° (point down)"),
    228: _MATRIX.format(answer="a hatched star turned 180° (point down)"),
    232: _MATRIX_SIZE.format(answer="a medium hatched pentagon turned 180° (point down)"),
    234: _MATRIX_SIZE.format(answer="a medium hatched triangle pointing down"),
    235: _MATRIX_SIZE.format(answer="a medium hatched circle"),
    237: _MATRIX_SIZE.format(answer="a medium hatched triangle pointing down"),
    239: _MATRIX.format(answer="a hatched pentagon turned 180° (point down)"),
    242: _MATRIX.format(answer="a hatched diamond (A is cross-hatched)"),
    245: _MATRIX.format(answer="a hatched pentagon turned 180° (point down)"),
    247: _MATRIX.format(answer="a hatched triangle pointing down"),
    248: _MATRIX.format(answer="a hatched square (D is turned 45°, which the matrix never does)"),
    250: _MATRIX_SIZE.format(answer="a medium hatched pentagon turned 180° (point down)"),
}


# ---------- reading the PDF ----------

def read_blueprint(doc):
    """Section B: {no: {materi, sub, level, key}} for all 250 questions."""
    start = next(i for i in range(len(doc)) if doc[i].get_text().lstrip().startswith("B. Blueprint"))
    text = ""
    for i in range(start, len(doc)):
        page = doc[i].get_text()
        if i > start and "SOAL NOMOR" in page:
            break
        text += page
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    i, rows = lines.index("Kunci") + 1, {}
    for n in range(1, 251):
        assert lines[i] == str(n), f"blueprint: expected row {n}, found {lines[i]!r}"
        j = i + 1
        while lines[j] not in ("mudah", "sedang", "sulit"):
            j += 1
        rows[n] = {"materi": lines[i + 1], "sub": " ".join(lines[i + 2:j]), "level": lines[j], "key": lines[j + 1]}
        i = j + 2
    return rows


def read_key_summary(doc):
    """Section D: {no: key}. The table alternates a row of ten numbers with a row of ten letters."""
    start = next(i for i in range(len(doc)) if doc[i].get_text().lstrip().startswith("D. Rekapitulasi"))
    text = ""
    for i in range(start, len(doc)):
        page = doc[i].get_text()
        if page.lstrip().startswith("E. "):
            break
        text += page
    tokens = [t.strip() for t in text.splitlines()[1:] if t.strip()]
    key, pending = {}, []
    for t in tokens:
        if t.isdigit():
            pending.append(int(t))
        elif re.fullmatch(r"[A-D]", t):
            key[pending.pop(0)] = t
    assert sorted(key) == list(range(1, 251)), "key summary does not cover 1–250"
    return key


def question_images(doc):
    """{no: xref} of the one embedded image under each "SOAL NOMOR n" heading."""
    images, current = {}, None
    for page in doc:
        events = [(b[1], 0, int(m.group(1))) for b in page.get_text("blocks")
                  for m in re.finditer(r"SOAL NOMOR (\d+)", b[4])]
        events += [(info["bbox"][1], 1, info["xref"]) for info in page.get_image_info(xrefs=True)]
        for _, kind, value in sorted(events):
            if kind == 0:
                current = value
            elif current is not None:
                assert current not in images, f"question {current} has more than one image"
                images[current] = value
    return images


# ---------- images ----------

def split_cells(strip):
    """The framed cells of a strip, left to right (each with its label underneath), as greyscale arrays."""
    a = np.asarray(strip.convert("L"))
    dark = (a < 200).any(axis=0)
    cells, x = [], 0
    while x < len(dark):
        if dark[x]:
            start = x
            while x < len(dark) and dark[x]:
                x += 1
            cells.append(strip.crop((start, 0, x, strip.height)))
        else:
            x += 1
    return cells


def relayout(strip, rows, skip_first):
    """Stimulus cells on `rows` rows (e.g. [3, 3, 3]), then a line, then the four options on one row."""
    cells = split_cells(strip)
    if skip_first:
        cells = cells[1:]
    assert len(cells) == sum(rows) + 4, f"{len(cells)} cells, expected {sum(rows) + 4}"
    w, h = max(c.width for c in cells), max(c.height for c in cells)
    columns = max(rows + [4])
    grid = []
    for count in rows:
        grid.append(cells[:count])
        cells = cells[count:]
    grid.append(cells)
    rule = 2 * GAP if rows else 0  # extra space and a line between the stimulus and the options
    width = columns * w + (columns + 1) * GAP
    height = len(grid) * h + (len(grid) + 1) * GAP + rule
    out = Image.new("RGB", (width, height), "white")
    y = GAP
    for r, row in enumerate(grid):
        if r == len(grid) - 1 and rows:
            line_y = y + GAP // 2
            out.paste((160, 160, 160), (GAP, line_y, width - GAP, line_y + 2))
            y += rule
        for c, cell in enumerate(row):
            out.paste(cell, (GAP + c * (w + GAP), y))
        y += h + GAP
    return out


def save_image(img, path):
    img.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)


# ---------- JSON ----------

def build_test(test, numbers, key):
    first, last, topic, title, text, _ = TOPICS[test]
    questions = []
    for i, n in enumerate(numbers, 1):
        q = {
            "id": f"L{test}-Q{i:02}",
            "text": text,
            "image": f"img/figbank-{n:03}.png",
            "imageAlt": f"Bank question {n} ({title.lower()}), with the answer options A–D drawn in the picture.",
            "sourceRef": f"Bank no. {n}",
            "options": {letter: f"Figure {letter}" for letter in OPTIONS},
            "answer": key[n],
        }
        if n in AMBIGUOUS:
            q["verifiedAnswer"] = None
            q["answerSource"] = "dropped"
        q["explanation"] = EXPLANATIONS.get(n, "")
        q["source"] = "imported"
        if n in AMBIGUOUS:
            q["flag"] = {"type": "ambiguous", "note": AMBIGUOUS[n]}
        elif n in DISPUTED:
            q["flag"] = {"type": "disputed", "note": DISPUTED[n]}
        questions.append(q)
    return {"id": f"L{test}", "section": "logic", "test": test, "title": f"Logic – {title} (imported)",
            "source": "imported", "questions": questions}


def selected(blueprint, test):
    first, last, topic, *_ = TOPICS[test]
    numbers = [n for n in range(first, last + 1) if blueprint[n]["level"] in LEVELS]
    assert all(blueprint[n]["materi"] == topic for n in numbers), f"topic mismatch in L{test}"
    assert len(numbers) == 17, f"L{test}: {len(numbers)} questions"
    return numbers


def write_images(doc, numbers_by_test):
    xrefs = question_images(doc)
    for test, numbers in numbers_by_test.items():
        rows = TOPICS[test][5]
        for n in numbers:
            info = doc.extract_image(xrefs[n])
            strip = Image.open(io.BytesIO(info["image"])).convert("RGB")
            save_image(relayout(strip, rows, skip_first=(test == 7)), IMG / f"figbank-{n:03}.png")


def main():
    doc = fitz.open(PDF)
    blueprint = read_blueprint(doc)
    summary = read_key_summary(doc)
    numbers_by_test = {test: selected(blueprint, test) for test in TOPICS}
    mismatches = [(n, blueprint[n]["key"], summary[n]) for ns in numbers_by_test.values() for n in ns
                  if blueprint[n]["key"] != summary[n]]
    assert not mismatches, f"section B and D keys differ: {mismatches}"
    write_images(doc, numbers_by_test)
    key = {n: row["key"] for n, row in blueprint.items()}
    for test, numbers in numbers_by_test.items():
        out = DATA / f"logic-{test}.json"
        out.write_text(json.dumps(build_test(test, numbers, key), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}: bank no. {', '.join(map(str, numbers))}")
    print(f"keys: section B and D agree for all {sum(map(len, numbers_by_test.values()))} imported questions")


if __name__ == "__main__":
    main()
