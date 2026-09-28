"""Build Logic subtest 5 (extra-hard figural patterns) from figural-test-extra-hard-part-1.

Copies the images into site/img/ and writes site/data/logic-5.json with the key from jawaban.txt.
The originals are left untouched. Images wider than MAX_WIDTH are scaled down (still sharp enough
for the small symbols), the alpha channel is dropped and the colours are reduced to a palette,
which keeps the page light.

"answer" is always the source key. It is also the scored answer, except for the OVERRIDES below (scored
answer set by review decision, in "verifiedAnswer"). Disagreements are flagged "disputed" (see REVIEW.md). The timer is not in the JSON: it is SECTIONS.logic.testMinutes[5] in site/js/data.js.

Run:  python tools/import_figural.py
"""
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "figural-test-extra-hard-part-1"
TARGET = ROOT / "site" / "img"
MAX_WIDTH = 1200
COUNT = 17

SERIES = "Which figure comes next in the series? The top row is the series; the options A–E are the bottom row."
SERIES_6 = ("Which figure comes next in the series? The options are not lettered in the picture: "
            "they are A–F from left to right{extra}.")
ANALOGY = "The first figure is to the second as the third is to ? Which option replaces the ? (options A–E)"
ANALOGY_2 = ("Which option replaces the ? so that the first pair of figures relates in the same way as the second pair? "
             "(options A–E)")

# number -> (question text, explanation); an empty explanation means I'm not confident of the rule (see REVIEW.md)
QUESTIONS = {
    1: (SERIES, "The arrow turns 90° then 45° anticlockwise in turn (down, right, up-right, up-left, left, so next is down), "
                "and the hook on the bar flips down/up each step, so next it points up."),
    2: (SERIES, "The four end symbols change order by 'move the first to the end' and 'swap the pairs' in turn, and the "
                "comb flips side each step; figure 5 equals figure 1, so figure 6 equals figure 2."),
    3: (SERIES, ""),
    4: (SERIES, ""),
    5: (SERIES, "Each figure is a polygon with one more side than the last, cut into as many regions as it has sides "
                "(3, 4, 5, 6, 7), so next is an 8-sided shape with 8 regions."),
    6: (SERIES, "Circle, triangle, square: each new shape first appears small inside the previous one, so next is a "
                "square with a small pentagon inside."),
    7: (SERIES, "On even frames the right side loses lines from the top: 1 line, then 3 lines, so next 5 lines are gone; "
                "the left side is full again."),
    8: (SERIES, "The arrow jumps two sectors clockwise each step, its direction cycling SE, SW, NW; the dot moves one "
                "sector clockwise each step."),
    9: (SERIES, ""),
    10: (SERIES, "One symbol moves each step, going 2, 3, 4, then 2 cells anticlockwise round the border; next the X moves "
                 "3 cells, to bottom-middle."),
    11: (SERIES, ""),
    12: (SERIES_6.format(extra=""), "Two squares on a diagonal alternate with four squares, and the diagonal switches each "
                                    "time; next is two squares top-left and bottom-right."),
    13: (SERIES_6.format(extra=""), ""),
    14: (SERIES_6.format(extra="; F is the one on the second row"),
         "One more dot and one more arrow each step (6 dots, 5 arrows next); the fan of arrows starts 45° further clockwise "
         "each time, so next it runs S, SW, W, NW, N."),
    15: (ANALOGY, "The large shape gets one more side and the two small shapes swap places (inside and outside), with the "
                  "outside one at the top right: a black pentagon holding a square, with a small pentagon outside."),
    16: (ANALOGY, "The large shape is joined by its shaded mirror image, and the rectangles become triangles with the "
                  "middle one still shaded."),
    17: (ANALOGY_2, "The small shapes above and below the block swap places and the shape inside the block loses a side "
                    "(pentagon to diamond), so the hexagon becomes a pentagon."),
}

# My solution differs from the source key: keep the key, show a note (reasoning in REVIEW.md).
DISPUTED = {
    11: "My answer is A: figure 5 is identical to figure 1, and each step turns either the middle bar or the top and "
        "bottom bars by 180°, so figure 6 should equal figure 2, which is option A. The source key gives B, whose middle "
        "bar bends up at the right instead. The site scores the source key (B).",
}

# The site scores a different answer than the source key, by review decision: number -> (scored letter, flag note).
# The source key stays in "answer"; the flag is "disputed".
OVERRIDES = {
    9: ("D", "Source key was C; this site scores D (the option with three closed ovals) by review decision. "
             "The rule behind D has not been written up yet."),
}


def read_key():
    text = (SOURCE / "jawaban.txt").read_text(encoding="utf-8")
    key = {int(n): letter for n, letter in re.findall(r"soal-(\d+)\.png \(([A-F])\)", text)}
    assert sorted(key) == list(range(1, COUNT + 1)), f"key covers {sorted(key)}"
    return key


def option_count(n):
    return 6 if n in (12, 13, 14) else 5  # jawaban.txt says "Soal pilihan A-F", but 15–17 print only A–E


def build_test(key):
    questions = []
    for n in range(1, COUNT + 1):
        text, explanation = QUESTIONS[n]
        letters = "ABCDEF"[:option_count(n)]
        q = {
            "id": f"L5-Q{n:02}",
            "text": text,
            "image": f"img/figural-hard-{n:02}.png",
            "imageAlt": f"Figure puzzle {n} from the imported extra-hard set, with the answer options drawn in the picture.",
            "options": {letter: f"Figure {letter}" for letter in letters},
            "answer": key[n],
        }
        if n in OVERRIDES:
            q["verifiedAnswer"] = OVERRIDES[n][0]
        q["explanation"] = explanation
        q["source"] = "imported"
        if n in DISPUTED:
            q["flag"] = {"type": "disputed", "note": DISPUTED[n]}
        elif n in OVERRIDES:
            q["flag"] = {"type": "disputed", "note": OVERRIDES[n][1]}
        questions.append(q)
    return {"id": "L5", "section": "logic", "test": 5, "title": "Logic – Figural patterns (extra hard)",
            "source": "imported", "questions": questions}


def copy_images():
    for n in range(1, COUNT + 1):
        src = SOURCE / f"soal-{n}.png"
        dst = TARGET / f"figural-hard-{n:02}.png"
        im = Image.open(src).convert("RGB")  # the sources are opaque screenshots with an alpha channel
        if im.width > MAX_WIDTH:
            im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)
        im.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(dst, optimize=True)
        print(f"{src.name:<12} {src.stat().st_size // 1024:>4} KB -> {dst.name} {im.size[0]}x{im.size[1]} "
              f"{dst.stat().st_size // 1024:>4} KB")


def main():
    copy_images()
    out = ROOT / "site" / "data" / "logic-5.json"
    out.write_text(json.dumps(build_test(read_key()), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
