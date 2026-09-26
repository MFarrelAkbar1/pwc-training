"""Generate the four Logic (TPA-style) subtests with computed answers.

  L1  Number sequences     rules from gen_sequences.py
  L2  Figure patterns      SVG images drawn here; the next figure is computed from the rule
  L3  Analogies            hand-written pairs, each tagged with its relation type
  L4  Syllogisms           answers found by checking every possible arrangement of the groups

Run:  python tools/gen_logic.py   (writes site/data/logic-1..4.json and site/img/logic/*.svg)
Everything is seeded, so re-running produces the same questions.
"""
import itertools
import json
import math
import random
from pathlib import Path
from xml.etree import ElementTree

import gen_sequences

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "data"
IMG = ROOT / "site" / "img" / "logic"
LETTERS = "ABCDE"
TIME = {1: 600, 2: 720, 3: 480, 4: 720}  # seconds per subtest (10 / 12 / 8 / 12 min)
TITLES = {1: "Number sequences", 2: "Figure patterns", 3: "Analogies", 4: "Syllogisms"}


def write_test(n, questions, note=None):
    test = {
        "id": f"L{n}",
        "section": "logic",
        "test": n,
        "title": f"Logic – {TITLES[n]}",
        "timeLimitSec": TIME[n],
        "source": "generated",
        "questions": questions,
    }
    if note:
        test["note"] = note
    path = DATA / f"logic-{n}.json"
    path.write_text(json.dumps(test, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path.name}: {len(questions)} questions")


def place(correct, wrong, rng, keep_last=None):
    """Shuffle options; return (options dict, answer letter). keep_last stays in slot E."""
    items = wrong + [correct]
    rng.shuffle(items)
    if keep_last is not None:
        items.append(keep_last)
    assert len(set(map(str, items))) == len(items), items
    return {LETTERS[i]: str(v) for i, v in enumerate(items)}, LETTERS[items.index(correct)]


# ====================================================================== L1

def build_sequences():
    rng = random.Random(101)
    rules = gen_sequences.RULES * 3
    rng.shuffle(rules)
    questions = []
    for n, rule in enumerate(rules[:15], start=1):
        q = gen_sequences.make_question(rng, n, rule, "L1")
        q.pop("rule")
        questions.append(q)
    write_test(1, questions)


# ====================================================================== L2 (SVG)

SYMMETRY = {"arrow": 360, "L": 360, "triangle": 120, "square": 90, "circle": 1}
DIRECTIONS = {0: "up", 45: "up-right", 90: "right", 135: "down-right", 180: "down",
              225: "down-left", 270: "left", 315: "up-left"}
CORNERS = ["top-left", "top-right", "bottom-right", "bottom-left"]  # clockwise order


def canonical(s):
    """Two figures that look identical have the same canonical form."""
    return (s["shape"], s["rot"] % SYMMETRY[s["shape"]], s["filled"], s["count"], s.get("corner"))


def describe(s):
    parts = [f"{s['count']} {'filled' if s['filled'] else 'outlined'} {s['shape']}{'s' if s['count'] > 1 else ''}"]
    if s["shape"] in ("arrow", "triangle") and s["rot"] % 360 in DIRECTIONS:
        parts.append(f"pointing {DIRECTIONS[s['rot'] % 360]}")
    elif s["shape"] == "L":
        parts.append(f"rotated {s['rot'] % 360}°")
    if s.get("corner") is not None:
        parts.append(f"dot {CORNERS[s['corner']]}")
    return ", ".join(parts)


def pattern_rotate(rng):
    shape, step, start = rng.choice(["arrow", "L"]), rng.choice([45, 90, 135]), rng.choice([0, 90, 180, 270])
    turn = rng.choice([1, -1])
    states = [dict(shape=shape, rot=(start + turn * step * i) % 360, filled=True, count=1, corner=None) for i in range(5)]
    way = "clockwise" if turn == 1 else "anticlockwise"
    return states, f"The {shape} turns {step}° {way} each step", step


def pattern_rotate_fill(rng):
    start, turn = rng.choice([0, 90, 180, 270]), rng.choice([1, -1])
    first_filled = rng.choice([True, False])
    states = [dict(shape="arrow", rot=(start + turn * 90 * i) % 360, filled=first_filled != (i % 2 == 1),
                   count=1, corner=None) for i in range(5)]
    way = "clockwise" if turn == 1 else "anticlockwise"
    return states, f"The arrow turns 90° {way} each step and the fill alternates", 90


def pattern_count_fill(rng):
    shape, start = rng.choice(["circle", "square"]), rng.choice([1, 2])
    first_filled = rng.choice([True, False])
    states = [dict(shape=shape, rot=0, filled=first_filled != (i % 2 == 1), count=start + i, corner=None, small=True)
              for i in range(5)]
    return states, f"One more {shape} is added each step and the fill alternates", 90


def pattern_corner_flip(rng):
    start, turn = rng.randrange(4), rng.choice([1, -1])
    first_rot = rng.choice([0, 180])
    states = [dict(shape="triangle", rot=(first_rot + 180 * i) % 360, filled=False, count=1,
                   corner=(start + turn * i) % 4) for i in range(5)]
    way = "clockwise" if turn == 1 else "anticlockwise"
    return states, f"The dot moves one corner {way} each step and the triangle flips each step", 180


def pattern_countdown_rotate(rng):
    start, turn = rng.choice([0, 90, 180, 270]), rng.choice([1, -1])
    states = [dict(shape="arrow", rot=(start + turn * 90 * i) % 360, filled=True, count=5 - i, corner=None, small=True)
              for i in range(5)]
    way = "clockwise" if turn == 1 else "anticlockwise"
    return states, f"One arrow disappears each step and the arrows turn 90° {way} each step", 90


PATTERNS = [pattern_rotate, pattern_rotate_fill, pattern_count_fill, pattern_corner_flip, pattern_countdown_rotate]


def pattern_distractors(answer, previous, step):
    """Figures that break exactly one part of the rule (plus 'the last figure again')."""
    variants = [dict(previous)]
    for delta in (step, -step, 180, 90):
        variants.append({**answer, "rot": (answer["rot"] + delta) % 360})
    variants.append({**answer, "filled": not answer["filled"]})
    for delta in (1, -1):
        if 1 <= answer["count"] + delta <= 6:
            variants.append({**answer, "count": answer["count"] + delta})
    if answer.get("corner") is not None:
        for delta in (1, 2, 3):
            variants.append({**answer, "corner": (answer["corner"] + delta) % 4})
    seen, out = {canonical(answer)}, []
    for v in variants:
        if canonical(v) not in seen:
            seen.add(canonical(v))
            out.append(v)
    return out


# ---- drawing ----

CELL, GAP, PAD = 84, 14, 12
INK = "#1f2933"


def shape_svg(shape, cx, cy, size, rot, filled):
    fill = INK if filled else "#ffffff"
    style = f'fill="{fill}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"'
    s = size
    if shape == "circle":
        return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{s * 0.8:.1f}" {style}/>'
    points = {
        "arrow": [(0, -s), (0.75 * s, -0.1 * s), (0.28 * s, -0.1 * s), (0.28 * s, s), (-0.28 * s, s),
                  (-0.28 * s, -0.1 * s), (-0.75 * s, -0.1 * s)],
        "L": [(-0.6 * s, -s), (-0.1 * s, -s), (-0.1 * s, 0.45 * s), (0.65 * s, 0.45 * s), (0.65 * s, s), (-0.6 * s, s)],
        "triangle": [(0, -s), (0.87 * s, 0.5 * s), (-0.87 * s, 0.5 * s)],
        "square": [(-0.7 * s, -0.7 * s), (0.7 * s, -0.7 * s), (0.7 * s, 0.7 * s), (-0.7 * s, 0.7 * s)],
    }[shape]
    a = math.radians(rot)
    pts = " ".join(f"{cx + x * math.cos(a) - y * math.sin(a):.1f},{cy + x * math.sin(a) + y * math.cos(a):.1f}"
                   for x, y in points)
    return f'<polygon points="{pts}" {style}/>'


LAYOUTS = {1: [(0, 0)], 2: [(-1, 0), (1, 0)], 3: [(-1, 1), (1, 1), (0, -1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
           5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (0, -1), (1, -1), (-1, 1), (0, 1), (1, 1)]}


def figure_svg(state, x, y):
    parts = [f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="8" fill="#ffffff" stroke="#9aa5b1" stroke-width="1.5"/>']
    cx, cy = x + CELL / 2, y + CELL / 2
    if state["count"] == 1 and not state.get("small"):
        parts.append(shape_svg(state["shape"], cx, cy, 24, state["rot"], state["filled"]))
    elif state["count"] == 1:  # same size as in the multi-shape figures, so size gives nothing away
        parts.append(shape_svg(state["shape"], cx, cy, 10.5, state["rot"], state["filled"]))
    else:
        spread = 21 if state["count"] <= 4 else 22
        for dx, dy in LAYOUTS[state["count"]]:
            parts.append(shape_svg(state["shape"], cx + dx * spread, cy + dy * spread * 0.95, 10.5, state["rot"], state["filled"]))
    if state.get("corner") is not None:
        ox, oy = [(10, 10), (CELL - 10, 10), (CELL - 10, CELL - 10), (10, CELL - 10)][state["corner"]]
        parts.append(f'<circle cx="{x + ox}" cy="{y + oy}" r="5.5" fill="{INK}"/>')
    return "".join(parts)


def pattern_svg(shown, options):
    width = PAD * 2 + 5 * CELL + 4 * GAP
    top, bottom = 26, 26 + CELL + 44
    height = bottom + CELL + 30
    def text(size=14, fill=INK, weight="400"):
        # each attribute exactly once: a repeated attribute makes the SVG invalid and it won't display
        return (f'font-family="system-ui, sans-serif" font-size="{size}" fill="{fill}" '
                f'font-weight="{weight}" text-anchor="middle"')
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
             f'<rect width="{width}" height="{height}" fill="#ffffff"/>']
    for i in range(5):
        x = PAD + i * (CELL + GAP)
        parts.append(f'<text x="{x + CELL / 2}" y="{top - 8}" {text()}>{i + 1 if i < 4 else "?"}</text>')
        if i < 4:
            parts.append(figure_svg(shown[i], x, top))
        else:
            parts.append(f'<rect x="{x}" y="{top}" width="{CELL}" height="{CELL}" rx="8" fill="#f1f4f7" '
                         f'stroke="#9aa5b1" stroke-width="1.5" stroke-dasharray="5 4"/>'
                         f'<text x="{x + CELL / 2}" y="{top + CELL / 2 + 9}" {text(28, "#9aa5b1")}>?</text>')
    parts.append(f'<line x1="{PAD}" x2="{width - PAD}" y1="{bottom - 24}" y2="{bottom - 24}" stroke="#d9dde3"/>')
    for i, state in enumerate(options):
        x = PAD + i * (CELL + GAP)
        parts.append(figure_svg(state, x, bottom))
        parts.append(f'<text x="{x + CELL / 2}" y="{bottom + CELL + 20}" {text(weight="700")}>{LETTERS[i]}</text>')
    parts.append("</svg>")
    return "".join(parts)


def build_patterns():
    rng = random.Random(202)
    IMG.mkdir(parents=True, exist_ok=True)
    families = PATTERNS * 3
    rng.shuffle(families)
    questions = []
    for n, family in enumerate(families, start=1):
        while True:
            states, rule_text, step = family(rng)
            shown, answer = states[:4], states[4]
            wrong = pattern_distractors(answer, shown[-1], step)
            if len(wrong) >= 4:
                break
        wrong = rng.sample(wrong[:6], 4) if len(wrong) > 4 else wrong
        order = wrong + [answer]
        rng.shuffle(order)
        keys = [canonical(s) for s in order]
        assert len(set(keys)) == 5 and keys.count(canonical(answer)) == 1
        qid = f"L2-Q{n:02d}"
        svg = pattern_svg(shown, order)
        ElementTree.fromstring(svg)  # raises if the SVG isn't valid XML (browsers then show nothing)
        (IMG / f"{qid}.svg").write_text(svg, encoding="utf-8")
        letter = LETTERS[order.index(answer)]
        questions.append({
            "id": qid,
            "text": "Which figure comes next in the sequence?",
            "image": f"img/logic/{qid}.svg",
            "imageAlt": "Figures 1 to 4: " + "; ".join(describe(s) for s in shown) +
                        ". Options: " + "; ".join(f"{LETTERS[i]}: {describe(s)}" for i, s in enumerate(order)) + ".",
            "options": {LETTERS[i]: f"Figure {LETTERS[i]}" for i in range(5)},
            "answer": letter,
            "explanation": f"{rule_text}, so figure 5 shows {describe(answer)} (option {letter}).",
            "source": "generated",
        })
    write_test(2, questions)


# ====================================================================== L3

# (relation type, pair A, pair B first word, correct, [4 wrong])
ANALOGIES = [
    ("synonym", ("Abundant", "Plentiful"), "Scarce", "Rare", ["Many", "Wealthy", "Empty", "Useful"]),
    ("antonym", ("Expand", "Contract"), "Increase", "Decrease", ["Grow", "Raise", "Multiply", "Maintain"]),
    ("part-whole", ("Page", "Book"), "Petal", "Flower", ["Stem", "Garden", "Leaf", "Colour"]),
    ("tool-function", ("Pen", "Write"), "Spade", "Dig", ["Garden", "Soil", "Plant", "Farmer"]),
    ("cause-effect", ("Rain", "Flood"), "Drought", "Famine", ["Desert", "Water", "Cloud", "Summer"]),
    ("category-member", ("Fruit", "Mango"), "Vehicle", "Truck", ["Road", "Engine", "Driver", "Wheel"]),
    ("synonym", ("Candid", "Frank"), "Diligent", "Industrious", ["Lazy", "Clever", "Wealthy", "Brave"]),
    ("antonym", ("Transparent", "Opaque"), "Permanent", "Temporary", ["Stable", "Fixed", "Lasting", "Solid"]),
    ("part-whole", ("Keyboard", "Laptop"), "Engine", "Car", ["Fuel", "Driver", "Road", "Speed"]),
    ("tool-function", ("Microscope", "Magnify"), "Scale", "Weigh", ["Cut", "Heat", "Count", "Draw"]),
    ("cause-effect", ("Virus", "Infection"), "Friction", "Heat", ["Surface", "Speed", "Oil", "Rubber"]),
    ("category-member", ("Mammal", "Whale"), "Bird", "Penguin", ["Bat", "Butterfly", "Feather", "Nest"]),
    ("antonym", ("Frugal", "Extravagant"), "Humble", "Arrogant", ["Modest", "Poor", "Quiet", "Kind"]),
    ("cause-effect", ("Exercise", "Fitness"), "Study", "Knowledge", ["Book", "School", "Teacher", "Exam"]),
    ("part-whole", ("Chapter", "Novel"), "Scene", "Play", ["Actor", "Stage", "Ticket", "Curtain"]),
]

RELATION_TEXT = {
    "synonym": "the two words mean the same",
    "antonym": "the two words are opposites",
    "part-whole": "the first is a part of the second",
    "tool-function": "the second is what the first is used to do",
    "cause-effect": "the first causes the second",
    "category-member": "the second is a member of the first category",
}


def build_analogies():
    rng = random.Random(303)
    questions = []
    for n, (relation, (a, b), c, correct, wrong) in enumerate(ANALOGIES, start=1):
        assert len(wrong) == 4 and correct not in wrong
        options, letter = place(correct, wrong, rng)
        questions.append({
            "id": f"L3-Q{n:02d}",
            "text": f"{a} : {b}  =  {c} : ?",
            "options": options,
            "answer": letter,
            "explanation": f"Relation: {relation} ({RELATION_TEXT[relation]}). {a} → {b}, so {c} → {correct}.",
            "source": "generated",
            "relation": relation,
        })
    write_test(3, questions)


# ====================================================================== L4 (checked by brute force)

# Statements: ("all"|"no"|"some"|"some_not", X, Y) over three terms indexed 0, 1, 2.
FORMS = {"all": "All {x} are {y}.", "no": "No {x} are {y}.",
         "some": "Some {x} are {y}.", "some_not": "Some {x} are not {y}."}

SYLLOGISMS = [
    # terms, premises, candidate conclusions (A–D)
    (["managers", "employees", "insured people"],
     [("all", 0, 1), ("all", 1, 2)],
     [("all", 2, 0), ("all", 0, 2), ("some_not", 1, 2), ("no", 0, 2)]),
    (["auditors", "sales staff", "trainees"],
     [("no", 0, 1), ("all", 2, 1)],
     [("some", 0, 2), ("all", 1, 2), ("no", 2, 0), ("some", 1, 0)]),
    (["reports", "documents", "confidential items"],
     [("all", 0, 1), ("some", 1, 2)],
     [("some", 0, 2), ("all", 2, 0), ("no", 0, 2), ("some_not", 2, 1)]),
    (["engineers", "managers", "graduates"],
     [("some", 0, 1), ("all", 1, 2)],
     [("all", 0, 2), ("some_not", 2, 0), ("no", 1, 0), ("some", 0, 2)]),
    (["analysts", "Excel users", "consultants"],
     [("all", 0, 1), ("some_not", 2, 1)],
     [("some_not", 2, 0), ("some_not", 0, 2), ("no", 2, 0), ("all", 1, 0)]),
    (["contractors", "permanent staff", "auditors"],
     [("no", 0, 1), ("some", 1, 2)],
     [("no", 2, 0), ("some", 0, 2), ("all", 2, 1), ("some_not", 2, 0)]),
    (["internal auditors", "certified employees", "finance staff"],
     [("all", 0, 1), ("some", 1, 2)],
     [("some", 0, 2), ("all", 2, 1), ("no", 0, 2), ("some", 2, 0)]),
    (["servers", "backed-up systems", "systems at risk of data loss"],
     [("all", 0, 1), ("no", 1, 2)],
     [("some", 0, 2), ("all", 2, 0), ("some_not", 1, 0), ("no", 0, 2)]),
    (["directors", "shareholders", "interns"],
     [("all", 0, 1), ("no", 1, 2)],
     [("no", 2, 0), ("some", 2, 0), ("all", 1, 0), ("some", 1, 2)]),
    (["suppliers", "local firms", "listed companies"],
     [("some", 0, 1), ("no", 1, 2)],
     [("no", 0, 2), ("some", 2, 0), ("all", 1, 0), ("some_not", 0, 2)]),
    (["trainees", "induction attendees", "auditors"],
     [("all", 0, 1), ("all", 2, 1)],
     [("all", 0, 2), ("some", 2, 0), ("no", 0, 2), ("some_not", 1, 0)]),
    (["laptops", "shared devices", "company assets"],
     [("no", 0, 1), ("some", 2, 0)],
     [("some_not", 2, 1), ("no", 2, 1), ("some", 1, 2), ("all", 0, 2)]),
    (["approved invoices", "paid invoices", "late invoices"],
     [("all", 0, 1), ("some", 1, 2)],
     [("some", 0, 2), ("no", 0, 2), ("all", 2, 0), ("some_not", 2, 1)]),
    (["employees", "part-time workers", "hourly-paid workers"],
     [("some", 0, 1), ("all", 1, 2)],
     [("all", 0, 2), ("no", 2, 0), ("some", 0, 2), ("some_not", 1, 2)]),
    (["auditors", "approvers", "managers"],
     [("no", 0, 1), ("all", 1, 2)],
     [("no", 2, 0), ("some", 0, 2), ("all", 2, 1), ("some_not", 2, 0)]),
]


def holds(statement, regions):
    """regions: set of 3-bit masks (which terms an individual belongs to) that are non-empty."""
    kind, x, y = statement
    has = lambda r, t: bool(r >> t & 1)
    if kind == "all":
        return not any(has(r, x) and not has(r, y) for r in regions)
    if kind == "no":
        return not any(has(r, x) and has(r, y) for r in regions)
    if kind == "some":
        return any(has(r, x) and has(r, y) for r in regions)
    return any(has(r, x) and not has(r, y) for r in regions)  # some_not


def valid(premises, conclusion):
    """True if the conclusion is true in every arrangement where the premises are true.
    Assumes each group has at least one member (standard for these tests)."""
    found_model = False
    for bits in range(1, 256):
        regions = {r for r in range(8) if bits >> r & 1}
        if not all(any(r >> t & 1 for r in regions) for t in range(3)):
            continue  # a group would be empty
        if all(holds(p, regions) for p in premises):
            found_model = True
            if not holds(conclusion, regions):
                return False
    assert found_model, "premises contradict each other"
    return True


def build_syllogisms():
    questions = []
    for n, (terms, premises, candidates) in enumerate(SYLLOGISMS, start=1):
        text = lambda s: FORMS[s[0]].format(x=terms[s[1]], y=terms[s[2]])
        validity = [valid(premises, c) for c in candidates]
        assert sum(validity) <= 1, f"L4-Q{n}: more than one valid conclusion"
        letter = LETTERS[validity.index(True)] if any(validity) else "E"
        options = {LETTERS[i]: text(c) for i, c in enumerate(candidates)}
        options["E"] = "None of these conclusions follows."
        if letter == "E":
            explanation = ("None follows: the premises leave open how the groups overlap. "
                           f"For example, '{text(candidates[0])}' could be true or false.")
        else:
            explanation = (f"'{options[letter]}' is true in every situation where both statements are true; "
                           "each other option can be false while the statements still hold.")
        questions.append({
            "id": f"L4-Q{n:02d}",
            "text": "Statements: " + " ".join(text(p) for p in premises) +
                    " Assuming the statements are true, which conclusion must follow?",
            "options": options,
            "answer": letter,
            "explanation": explanation,
            "source": "generated",
        })
    write_test(4, questions)


if __name__ == "__main__":
    build_sequences()
    build_patterns()
    build_analogies()
    build_syllogisms()
