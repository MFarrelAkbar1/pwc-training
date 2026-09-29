"""Generate the Logic (TPA-style) subtests with computed answers.

  L1  Number sequences     rules from gen_sequences.py
  L2  Figure patterns      SVG images drawn here; the next figure is computed from the rule
  L3  Analogies            hand-written pairs, each tagged with its relation type
  L4  Syllogisms           answers found by checking every possible arrangement of the groups
  L11, L12  Number sequences 2, 3   hand-picked rules; answer computed, rival rules checked (see SEQUENCE_SETS)
  L13, L14  Analogies 2, 3          hand-written like L3 (checked by a blind pass, see REVIEW.md)
  L15, L16  Syllogisms 2, 3         like L4, with 3-premise questions; every option checked by brute force

L5–L10 are imported figural tests (tools/import_figural*.py), not built here.

Run:  python tools/gen_logic.py   (writes site/data/logic-{1..4,11..16}.json and site/img/logic/*.svg)
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
# seconds per subtest (10 / 12 / 8 / 12 min); the later sets keep the pace of their topic's first set
TIME = {1: 600, 2: 720, 3: 480, 4: 720, 11: 600, 12: 600, 13: 480, 14: 480, 15: 720, 16: 720}
TITLES = {1: "Number sequences", 2: "Figure patterns", 3: "Analogies", 4: "Syllogisms",
          11: "Number sequences 2", 12: "Number sequences 3", 13: "Analogies 2", 14: "Analogies 3",
          15: "Syllogisms 2", 16: "Syllogisms 3"}


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


# ====================================================================== L11–L16: second and third sets
# Same format, option count and timers as L1 / L3 / L4. Differences from the first sets:
#   - every question has a "difficulty" (easy / medium / hard); DIFFICULTY_MIX gives the count per set,
#     and the second set of each topic is a little harder (one easy question swapped for a medium one,
#     and harder rules / more 3-premise questions within each level);
#   - the answer letters are spread evenly (A–E three times each), because the first sets are lopsided;
#   - every question has its own explanation (L4's are generic).
# Checks that run on every build are marked "check:" and stop the build with an AssertionError.

from fractions import Fraction

NEW_SETS = {"sequences": (11, 12), "analogies": (13, 14), "syllogisms": (15, 16)}
DIFFICULTY_MIX = {0: {"easy": 5, "medium": 7, "hard": 3},   # first new set of a topic
                  1: {"easy": 4, "medium": 8, "hard": 3}}   # second (harder) set
MAX_CORRECT_LONGEST = 3  # check: the correct option may be the unique longest in at most 3 of 15 questions
REPORT = []  # what the checks rejected while building (printed at the end)


def balanced_letters(rng, count, letters):
    """Answer letters for a set: each letter equally often (count must divide evenly), in random order."""
    assert count % len(letters) == 0
    out = list(letters) * (count // len(letters))
    rng.shuffle(out)
    return out


def arrange(correct, wrong, letter, rng):
    """Options dict (A, B, …) with `correct` at `letter` and the wrong options, shuffled, in the other slots."""
    wrong = list(wrong)
    rng.shuffle(wrong)
    slot = LETTERS.index(letter)
    items = wrong[:slot] + [correct] + wrong[slot:]
    assert len(set(map(str, items))) == len(items), items
    return {LETTERS[i]: str(v) for i, v in enumerate(items)}


def check_set(test_id, questions, level):
    """check: size, difficulty mix, even answer letters, no length giveaway, explanations present."""
    assert len(questions) == 15, test_id
    mix = {d: sum(q["difficulty"] == d for q in questions) for d in ("easy", "medium", "hard")}
    assert mix == DIFFICULTY_MIX[level], (test_id, mix)
    letters = {x: sum(q["answer"] == x for q in questions) for x in LETTERS}
    assert set(letters.values()) == {3}, (test_id, letters)
    longest = 0
    for q in questions:
        assert q["explanation"].strip() and list(q["options"]) == list(LETTERS), q["id"]
        lengths = {k: len(v) for k, v in q["options"].items()}
        top = max(lengths.values())
        longest += lengths[q["answer"]] == top and list(lengths.values()).count(top) == 1
    assert longest <= MAX_CORRECT_LONGEST, f"{test_id}: correct option is the unique longest in {longest} questions"
    REPORT.append(f"{test_id}: answers {letters}, difficulty {mix}, correct option uniquely longest in {longest}/15")


# ---------------------------------------------------------------- L11, L12 number sequences
# Each question: (difficulty, full sequence, index of the hidden term, [4 wrong options], explanation).
# The sequence is computed from its rule by the helpers below, so the answer is whatever the rule gives.
# Wrong options are hand-picked slips (repeating the last step, the wrong one of two series, the wrong
# operation, averaging the neighbours, …).

def arith(a, d, n):
    return [a + d * i for i in range(n)]


def geom(a, r, n):
    return [Fraction(a) * Fraction(r) ** i for i in range(n)]


def from_diffs(a, diffs):
    seq = [a]
    for d in diffs:
        seq.append(seq[-1] + d)
    return seq


def alternate_ops(a, ops, n):
    """ops: e.g. [("×", 2), ("+", 3)], applied in turn."""
    seq = [a]
    for i in range(n - 1):
        op, k = ops[i % len(ops)]
        seq.append(seq[-1] * k if op == "×" else seq[-1] + k if op == "+" else seq[-1] - k)
    return seq


def interleave(first, second, n):
    seq = []
    for a, b in zip(first, second):
        seq += [a, b]
    return seq[:n]


def additive(start, n, window=2):
    """Each term is the sum of the `window` terms before it (Fibonacci-like; window 3 = 'tribonacci')."""
    seq = list(start)
    while len(seq) < n:
        seq.append(sum(seq[-window:]))
    return seq


def primes_from(first, n):
    out, k = [], first
    while len(out) < n:
        if k > 1 and all(k % p for p in range(2, int(k ** 0.5) + 1)):
            out.append(k)
        k += 1
    return out


def fractions(pairs):
    return [Fraction(a, b) for a, b in pairs]


SEQUENCE_SETS = {
    11: [
        ("easy", arith(7, 6, 6), 5, [38, 39, 41, 43],
         "Add 6 each time: 31 + 6 = 37."),
        ("easy", geom(3, 2, 6), 5, [72, 84, 94, 95],
         "Multiply by 2 each time: 48 × 2 = 96. (72 comes from adding the last difference, 24, again.)"),
        ("easy", arith(50, -6, 6), 2, [36, 39, 40, 42],
         "Subtract 6 each time: 44 − 6 = 38, and 38 − 6 = 32 fits the next term."),
        ("easy", [n * n for n in range(2, 8)], 5, [47, 48, 50, 64],
         "Square numbers: 2², 3², 4², 5², 6², so next is 7² = 49 (the differences 5, 7, 9, 11 grow by 2: 36 + 13)."),
        ("easy", interleave(arith(2, 2, 4), arith(10, 10, 4), 7), 6, [9, 10, 12, 40],
         "Two series alternate: 2, 4, 6, … (+2) and 10, 20, 30, … (+10). The 7th term belongs to the first "
         "series: 6 + 2 = 8. (40 continues the wrong series.)"),
        ("medium", from_diffs(3, [2, 4, 6, 8, 10, 12]), 6, [41, 43, 44, 47],
         "The differences are 2, 4, 6, 8, 10, so the next difference is 12: 33 + 12 = 45."),
        ("medium", alternate_ops(1, [("×", 2), ("+", 3)], 7), 6, [28, 31, 39, 52],
         "Alternate '× 2' and '+ 3': 1 × 2 = 2, + 3 = 5, × 2 = 10, + 3 = 13, × 2 = 26, so next is 26 + 3 = 29. "
         "(52 repeats the × 2.)"),
        ("medium", additive([2, 5], 7), 6, [38, 43, 48, 49],
         "Each term is the sum of the two before it: 19 + 31 = 50."),
        ("medium", [n * n + 1 for n in range(1, 7)], 3, [14, 15, 16, 18],
         "Square numbers + 1: 1²+1, 2²+1, 3²+1, so the missing term is 4² + 1 = 17. Check: the differences "
         "3, 5, 7, 9, 11 grow by 2 (10 + 7 = 17, 17 + 9 = 26)."),
        ("medium", primes_from(13, 6), 5, [32, 33, 35, 37],
         "Consecutive prime numbers: 13, 17, 19, 23, 29, and the next prime is 31 (30 and 32 are even, "
         "33 = 3 × 11, 35 = 5 × 7)."),
        ("medium", fractions([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]), 4, ["4/7", "5/7", "6/7", "6/5"],
         "Numerator and denominator each go up by 1 (n / (n + 1)): after 4/5 comes 5/6."),
        ("medium", [n ** 3 for n in range(1, 6)], 2, [16, 24, 32, 36],
         "Cube numbers: 1³ = 1, 2³ = 8, 3³ = 27, 4³ = 64, 5³ = 125. The missing term is 27."),
        ("hard", from_diffs(3, [1, 2, 4, 8, 16, 32]), 6, [50, 52, 58, 64],
         "The differences double: 1, 2, 4, 8, 16, so the next difference is 32: 34 + 32 = 66. "
         "(Same as 'double and subtract 2': 34 × 2 − 2 = 66.)"),
        ("hard", interleave(arith(5, 3, 4), arith(40, -5, 4), 7), 5, [14, 25, 27, 32],
         "Two series alternate: 5, 8, 11, 14 (+3) and 40, 35, ?, … (−5). The gap is in the second series: "
         "35 − 5 = 30. (14 belongs to the first series.)"),
        ("hard", fractions([(n, n + 2) for n in range(1, 6)]), 4, ["4/7", "3/4", "5/6", "6/7"],
         "The terms are n / (n + 2): 1/3, 2/4 (= 1/2), 3/5, 4/6 (= 2/3), so next is 5/7. "
         "(3/4 is the n / (n + 1) pattern, which doesn't fit 1/3.)"),
    ],
    12: [
        ("easy", arith(81, -7, 6), 5, [39, 44, 45, 47],
         "Subtract 7 each time: 53 − 7 = 46."),
        ("easy", geom(3, 4, 5), 2, [21, 24, 96, 102],
         "Multiply by 4 each time: 12 × 4 = 48, and 48 × 4 = 192 fits the next term. "
         "(102 is the average of 12 and 192, which only works for adding.)"),
        ("easy", geom(800, Fraction(1, 2), 6), 5, [20, 30, 35, 40],
         "Halve each time: 50 ÷ 2 = 25."),
        ("easy", [n * (n + 1) for n in range(1, 7)], 5, [44, 48, 50, 60],
         "The differences are 4, 6, 8, 10, so the next is 12: 30 + 12 = 42 (each term is n × (n + 1): 6 × 7)."),
        ("medium", alternate_ops(2, [("×", 3), ("−", 2)], 7), 6, [29, 30, 32, 90],
         "Alternate '× 3' and '− 2': 2 × 3 = 6, − 2 = 4, × 3 = 12, − 2 = 10, × 3 = 30, so next is 30 − 2 = 28. "
         "(90 repeats the × 3.)"),
        ("medium", from_diffs(4, [3, 6, 9, 12, 15]), 3, [16, 19, 20, 21],
         "The differences go up by 3: 3, 6, 9, 12, 15. So the missing term is 13 + 9 = 22, and 22 + 12 = 34 fits."),
        ("medium", additive([3, 4], 7), 4, [15, 16, 20, 22],
         "Each term is the sum of the two before it: 7 + 11 = 18, and 11 + 18 = 29, 18 + 29 = 47 fit."),
        ("medium", [n ** 3 - 1 for n in range(1, 7)], 5, [185, 216, 217, 248],
         "Cube numbers − 1: 1³−1, 2³−1, …, 5³−1 = 124, so next is 6³ − 1 = 215. "
         "(216 forgets the − 1.)"),
        ("medium", [2 * p for p in primes_from(2, 7)], 6, [17, 28, 30, 38],
         "Double the prime numbers: 2×2, 2×3, 2×5, 2×7, 2×11, 2×13, so next is 2 × 17 = 34."),
        ("medium", geom(Fraction(2, 3), Fraction(2, 3), 5), 4, ["32/729", "16/243", "64/243", "32/81"],
         "Multiply by 2/3 each time (numerators × 2, denominators × 3): 16/81 × 2/3 = 32/243."),
        ("medium", interleave([3 * 2 ** i for i in range(4)], arith(20, -3, 4), 8), 7, [12, 13, 17, 48],
         "Two series alternate: 3, 6, 12, 24 (× 2) and 20, 17, 14, … (− 3). The 8th term belongs to the second "
         "series: 14 − 3 = 11. (48 continues the first series.)"),
        ("medium", from_diffs(1, [1, 3, 9, 27, 81]), 5, [68, 123, 124, 164],
         "The differences are powers of 3: 1, 3, 9, 27, so the next is 81: 41 + 81 = 122. "
         "(Same as '× 3 − 1': 41 × 3 − 1 = 122.)"),
        ("hard", additive([1, 1, 2], 8, window=3), 7, [35, 37, 41, 43],
         "Each term is the sum of the three before it: 7 + 13 + 24 = 44. (37 adds only the last two.)"),
        ("hard", alternate_ops(3, [("+", 5), ("×", 2)], 7), 4, [26, 34, 37, 105],
         "Alternate '+ 5' and '× 2': 3 + 5 = 8, × 2 = 16, + 5 = 21, so the missing term is 21 × 2 = 42; "
         "then 42 + 5 = 47 and 47 × 2 = 94 fit."),
        ("hard", fractions([(2 ** n - 1, 2 ** n) for n in range(1, 6)]), 2, ["5/8", "11/16", "13/16", "5/6"],
         "Each term is 1 − 1/2ⁿ: 1/2, 3/4, 7/8, 15/16, 31/32 (the denominator doubles and the numerator is one "
         "less). The missing term is 7/8. (5/6 is the n / (n + 1) pattern.)"),
    ],
}


# ---- rival rules: each takes the full sequence (with a candidate filled in) and says whether it fits.
# A rule must be over-determined (at least two terms that it didn't need to fix its parameters),
# so that it can't fit by accident.

def _diffs(xs):
    return [b - a for a, b in zip(xs, xs[1:])]


def fits_polynomial(xs, degree):
    """Constant (degree+1)-th differences: degree 1 = arithmetic, 2 = constant second differences, 3 = cubic."""
    if len(xs) < degree + 3:
        return False
    d = xs
    for _ in range(degree + 1):
        d = _diffs(d)
    return all(v == 0 for v in d)


def fits_geometric(xs):
    return len(xs) >= 4 and all(x != 0 for x in xs[:-1]) and len({b / a for a, b in zip(xs, xs[1:])}) == 1


def fits_affine(xs):
    """Every term is m × previous + c (covers '× 3 − 1', differences growing by a constant factor, …)."""
    pairs = list(zip(xs, xs[1:]))
    if len(pairs) < 4:
        return False
    for (a0, a1), (b0, b1) in itertools.combinations(pairs, 2):
        if a0 != b0:
            m = (b1 - a1) / (b0 - a0)
            c = a1 - m * a0
            return all(y == m * x + c for x, y in pairs)
    return False


def fits_alternating_ops(xs):
    """Two simple operations (+k or ×k) applied in turn, e.g. × 2, + 3, × 2, + 3."""
    steps = list(zip(xs, xs[1:]))
    if len(steps) < 4:
        return False
    for parity in (0, 1):
        group = steps[parity::2]
        same_add = len({b - a for a, b in group}) == 1
        same_mul = all(a != 0 for a, _ in group) and len({b / a for a, b in group}) == 1
        if not (same_add or same_mul):
            return False
    return True


def fits_interleaved(xs):
    """Odd and even positions are each an arithmetic or geometric series (at least 3 terms each)."""
    if len(xs) < 6:
        return False
    for part in (xs[0::2], xs[1::2]):
        arithmetic = len(set(_diffs(part))) == 1
        geometric = all(x != 0 for x in part) and len({b / a for a, b in zip(part, part[1:])}) == 1
        if not (arithmetic or geometric):
            return False
    return True


def fits_recurrence2(xs):
    """Every term is p × (term before) + q × (term two before): Fibonacci-like with any weights."""
    eqs = [(xs[i - 1], xs[i - 2], xs[i]) for i in range(2, len(xs))]
    if len(eqs) < 4:
        return False
    for (a1, a2, a), (b1, b2, b) in itertools.combinations(eqs, 2):
        det = a1 * b2 - a2 * b1
        if det != 0:
            p, q = (a * b2 - a2 * b) / det, (a1 * b - a * b1) / det
            return all(z == p * x + q * y for x, y, z in eqs)
    return False


def fits_tribonacci(xs):
    return len(xs) >= 5 and all(xs[i] == xs[i - 1] + xs[i - 2] + xs[i - 3] for i in range(3, len(xs)))


PRIMES = primes_from(2, 60)


def fits_primes(xs):
    """Consecutive primes, times 1–3, plus or minus up to 10."""
    if len(xs) < 4 or any(x.denominator != 1 for x in map(Fraction, xs)):
        return False
    for m in (1, 2, 3):
        for c in range(-10, 11):
            for s in range(len(PRIMES) - len(xs)):
                if all(x == m * PRIMES[s + i] + c for i, x in enumerate(xs)):
                    return True
    return False


def fits_powers(xs):
    """n², n³ or 2ⁿ (from some starting n), plus or minus a constant; also n × (n + 1)."""
    if len(xs) < 4:
        return False
    for f in (lambda n: n * n, lambda n: n ** 3, lambda n: 2 ** n, lambda n: n * (n + 1)):
        for s in range(0, 12):
            c = xs[0] - f(s)
            if all(x == f(s + i) + c for i, x in enumerate(xs)):
                return True
    return False


def _value_rules(xs):
    rules = {"arithmetic": fits_polynomial(xs, 1), "second differences": fits_polynomial(xs, 2),
             "cubic": fits_polynomial(xs, 3), "geometric": fits_geometric(xs), "m*prev+c": fits_affine(xs),
             "alternating operations": fits_alternating_ops(xs), "two interleaved series": fits_interleaved(xs),
             "weighted Fibonacci": fits_recurrence2(xs), "tribonacci": fits_tribonacci(xs),
             "primes": fits_primes(xs), "powers": fits_powers(xs)}
    return [name for name, ok in rules.items() if ok]


def rival_rules(xs):
    """Every simple rule the whole sequence fits. For fractions, also numerator and denominator rules
    (each read as shown, i.e. in lowest terms)."""
    xs = [Fraction(x) for x in xs]
    found = _value_rules(xs)
    if any(x.denominator != 1 for x in xs):
        nums, dens = _value_rules([x.numerator for x in xs]), _value_rules([x.denominator for x in xs])
        if nums and dens:
            found.append(f"numerators {nums[0]}, denominators {dens[0]}")
    return found


def check_rival_rules():
    """check: the rival-rule detectors themselves work (so a clean result means something)."""
    assert "arithmetic" in rival_rules([2, 4, 6, 8, 10, 12])
    assert "second differences" in rival_rules([2, 5, 10, 17, 26, 37])
    assert "geometric" in rival_rules([3, 6, 12, 24, 48])
    assert "two interleaved series" in rival_rules([1, 10, 2, 20, 3, 30, 4])
    assert "alternating operations" in rival_rules([1, 3, 6, 8, 16, 18])
    assert "weighted Fibonacci" in rival_rules([1, 2, 3, 5, 8, 13, 21])
    assert "primes" in rival_rules([3, 5, 7, 11, 13])
    assert not rival_rules([1, 2, 4, 8, 16, 31])


def fmt(x):
    return str(Fraction(x))


def sequence_question(test_id, n, spec, letter, rng):
    level, seq, hide, wrong, explanation = spec
    seq = [Fraction(x) for x in seq]
    answer = seq[hide]
    wrong = [Fraction(w) for w in wrong]
    shown = [fmt(x) if i != hide else "?" for i, x in enumerate(seq)]
    # check: the answer is what the rule gives; exactly one option has that value; the options are distinct
    assert len(wrong) == 4 and len(set(wrong)) == 4 and answer not in wrong, (test_id, n)
    assert fmt(answer) in explanation, f"{test_id}-Q{n:02d}: explanation doesn't state the answer {fmt(answer)}"
    # check: no rival rule fits the sequence with a wrong option filled in
    for w in wrong:
        rivals = rival_rules(seq[:hide] + [w] + seq[hide + 1:])
        assert not rivals, f"{test_id}-Q{n:02d}: option {fmt(w)} also fits: {rivals}"
    options = arrange(fmt(answer), [fmt(w) for w in wrong], letter, rng)
    first = "What number comes next?  " if hide == len(seq) - 1 else "What number is missing?  "
    return {
        "id": f"{test_id}-Q{n:02d}",
        "text": first + ",  ".join(shown),
        "options": options,
        "answer": letter,
        "explanation": explanation,
        "source": "generated",
        "difficulty": level,
    }, seq, answer


def answer_rank(q):
    """1 = the correct option is the smallest value, 5 = the largest (a spread check: not always the middle)."""
    values = sorted(Fraction(v) for v in q["options"].values())
    return values.index(Fraction(q["options"][q["answer"]])) + 1


def build_new_sequences():
    check_rival_rules()
    old = [json.loads((DATA / "logic-1.json").read_text(encoding="utf-8"))["questions"]]
    old_runs = set()
    for q in old[0]:
        terms = [t.strip() for t in q["text"].split("?", 1)[1].split(",") if t.strip() != "?"]
        old_runs |= {tuple(terms[i:i + 4]) for i in range(len(terms) - 3)}
    for level, test in enumerate(NEW_SETS["sequences"]):
        rng = random.Random(1100 + test)
        letters = balanced_letters(rng, 15, LETTERS)
        questions, ranks = [], []
        for n, spec in enumerate(SEQUENCE_SETS[test], start=1):
            q, seq, answer = sequence_question(f"L{test}", n, spec, letters[n - 1], rng)
            # check: not a copy of an L1 question or of an earlier new one (no 4 shown terms in a row in common)
            terms = [fmt(x) for x in seq]
            runs = {tuple(terms[i:i + 4]) for i in range(len(terms) - 3)}
            assert not runs & old_runs, f"{q['id']}: repeats a run of terms from an earlier question"
            old_runs |= runs
            # the intended rule should itself be one of the simple rules (or be a known pattern)
            if not rival_rules(seq):
                REPORT.append(f"{q['id']}: intended rule isn't in the rival-rule list (checked by hand)")
            ranks.append(answer_rank(q))
            questions.append(q)
        # check: the correct value isn't predictably the middle (or the smallest / largest) option
        spread = {r: ranks.count(r) for r in range(1, 6)}
        assert max(spread.values()) <= 4, f"L{test}: correct option's rank by value {spread}"
        REPORT.append(f"L{test}: rank of the correct value among the 5 options (1 = smallest) {spread}")
        check_set(f"L{test}", questions, level)
        write_test(test, questions)


# ---------------------------------------------------------------- L13, L14 analogies (format of L3)

RELATION_TEXT.update({
    "tool-user": "the first is a tool used by the second",
    "degree": "the second is a stronger form of the first",
    "function": "the first is used for the second",
    "sequence": "the second comes right after the first",
    "effect-cause": "the first is left behind by (is the result of) the second",
})

# (difficulty, relation, pair A, pair B first word, correct, [4 wrong], why the tempting wrong option fails)
ANALOGY_SETS = {
    13: [
        ("easy", "antonym", ("Ancient", "Modern"), "Victory", "Defeat", ["Battle", "Trophy", "Success", "Army"],
         "'Success' means nearly the same as victory, not the opposite."),
        ("easy", "part-whole", ("Finger", "Hand"), "Toe", "Foot", ["Shoe", "Nail", "Walk", "Sock"],
         "A nail is part of the toe: the relation the wrong way round."),
        ("easy", "tool-user", ("Stethoscope", "Doctor"), "Brush", "Painter", ["Canvas", "Paint", "Wall", "Colour"],
         "Canvas and paint are what the brush is used on or with, not the person who uses it."),
        ("easy", "category-member", ("Metal", "Iron"), "Colour", "Blue", ["Paint", "Bright", "Rainbow", "Light"],
         "A rainbow contains colours but isn't one; 'bright' describes a colour."),
        ("easy", "sequence", ("Monday", "Tuesday"), "March", "April", ["February", "Month", "Spring", "May"],
         "February comes before March and May two months after; only April comes straight after."),
        ("medium", "degree", ("Warm", "Hot"), "Cool", "Cold", ["Ice", "Winter", "Breeze", "Wet"],
         "Ice and winter are cold things, not a stronger word for 'cool'."),
        ("medium", "synonym", ("Brief", "Short"), "Vast", "Huge", ["Empty", "Narrow", "Distant", "Ocean"],
         "An ocean is vast, but it is an example, not a word with the same meaning."),
        ("medium", "function", ("Refrigerator", "Cool"), "Oven", "Bake", ["Kitchen", "Bread", "Chef", "Electricity"],
         "Bread is what gets baked and a kitchen is where the oven is; neither is what the oven does."),
        ("medium", "part-whole", ("Brick", "Wall"), "Link", "Chain", ["Metal", "Ring", "Lock", "Rope"],
         "Metal is what a link is made of (material), not the whole it is part of."),
        ("medium", "antonym", ("Generous", "Stingy"), "Cautious", "Reckless", ["Careful", "Nervous", "Slow", "Wise"],
         "'Careful' is a synonym of cautious; the opposite is reckless."),
        ("medium", "tool-user", ("Baton", "Conductor"), "Scalpel", "Surgeon",
         ["Hospital", "Patient", "Knife", "Operation"],
         "The patient is who the scalpel is used on, and an operation is what it is used for; the user is the surgeon."),
        ("medium", "cause-effect", ("Overeating", "Obesity"), "Insomnia", "Fatigue", ["Bed", "Night", "Dream", "Pillow"],
         "Insomnia (not being able to sleep) leads to fatigue; the other options are only linked to sleep."),
        ("hard", "antonym", ("Conceal", "Reveal"), "Scatter", "Gather", ["Spread", "Hide", "Break", "Sow"],
         "'Spread' is close to scatter, and 'hide' copies the first pair's word; the opposite of scatter is gather."),
        ("hard", "degree", ("Nibble", "Devour"), "Glance", "Stare", ["Look", "Blink", "Ignore", "Eye"],
         "'Look' is the neutral word; a stare is the long, intense form of a glance, as devouring is of nibbling."),
        ("hard", "function", ("Ruler", "Length"), "Clock", "Time", ["Hour", "Alarm", "Wall", "Watch"],
         "A ruler measures length, a clock measures time. An hour is a unit of time (like a centimetre), "
         "and a watch is another clock."),
    ],
    14: [
        ("easy", "synonym", ("Begin", "Start"), "Finish", "End", ["Race", "Goal", "Winner", "Line"],
         "A race has a finish, but only 'end' means the same as finish."),
        ("easy", "cause-effect", ("Cut", "Bleeding"), "Burn", "Blister", ["Fire", "Heat", "Bandage", "Skin"],
         "Fire and heat cause a burn (the wrong direction); a burn causes a blister."),
        ("easy", "category-member", ("Tree", "Oak"), "Flower", "Rose", ["Petal", "Garden", "Seed", "Bee"],
         "A petal is part of a flower, not a kind of flower."),
        ("easy", "part-whole", ("Leaf", "Tree"), "Feather", "Bird", ["Fly", "Sky", "Nest", "Light"],
         "A nest is where a bird lives and 'fly' is what it does; the feather is part of the bird."),
        ("medium", "tool-user", ("Plough", "Farmer"), "Whistle", "Referee", ["Sound", "Match", "Ball", "Stadium"],
         "A whistle makes a sound and is used in a match, but the person who uses it is the referee."),
        ("medium", "function", ("Umbrella", "Rain"), "Helmet", "Injury", ["Strap", "Bicycle", "Soldier", "Plastic"],
         "An umbrella protects against rain; a helmet protects against injury. A soldier or cyclist wears it, "
         "and plastic and a strap are what it is made of."),
        ("medium", "degree", ("Whisper", "Shout"), "Drizzle", "Downpour", ["Cloud", "Umbrella", "Puddle", "Mist"],
         "Mist is even lighter than a drizzle; a downpour is the heavy form, as a shout is of a whisper."),
        ("medium", "antonym", ("Shallow", "Deep"), "Rare", "Common", ["Unusual", "Precious", "Valuable", "Few"],
         "'Unusual' is a synonym of rare; the opposite is common."),
        ("medium", "sequence", ("Egg", "Chick"), "Seed", "Sprout", ["Soil", "Fruit", "Flower", "Water"],
         "A chick is the next stage after an egg, and a sprout the next stage after a seed. A flower comes "
         "later, and fruit contains the seed."),
        ("medium", "cause-effect", ("Bacteria", "Decay"), "Wind", "Erosion", ["Storm", "Sail", "Air", "Breeze"],
         "A breeze and a storm are kinds of wind, not results of it; wind wears rock away (erosion)."),
        ("medium", "part-whole", ("Verse", "Song"), "Ingredient", "Recipe", ["Chef", "Kitchen", "Taste", "Oven"],
         "A verse is one part of a song; an ingredient is one part of a recipe. The chef and kitchen are who and "
         "where."),
        ("medium", "synonym", ("Hostile", "Unfriendly"), "Hesitant", "Reluctant",
         ["Impatient", "Confident", "Hidden", "Eager"],
         "'Eager' and 'confident' are near-opposites of hesitant; reluctant means the same."),
        ("hard", "degree", ("Content", "Ecstatic"), "Uneasy", "Terrified", ["Calm", "Nervous", "Curious", "Courageous"],
         "'Nervous' is about as strong as uneasy; terrified is the extreme form, as ecstatic is of content."),
        ("hard", "effect-cause", ("Ash", "Fire"), "Scar", "Wound", ["Skin", "Doctor", "Bandage", "Face"],
         "Ash is what a fire leaves behind; a scar is what a wound leaves behind. Skin and face are where the "
         "scar is."),
        ("hard", "function", ("Anchor", "Ship"), "Leash", "Dog", ["Owner", "Walk", "Park", "Rope"],
         "An anchor holds a ship in place; a leash holds a dog in place. The owner holds the leash (the user, "
         "not the thing held), a walk and a park are where it is used, and rope is what a leash is like."),
    ],
}


def build_new_analogies():
    old_pairs = {(a, b) for _, (a, b), *_ in ANALOGIES}
    seen_words = {w for _, (a, b), c, d, _ in ANALOGIES for w in (a, b, c, d)}
    for level, test in enumerate(NEW_SETS["analogies"]):
        rng = random.Random(1300 + test)
        letters = balanced_letters(rng, 15, LETTERS)
        questions = []
        for n, (difficulty, relation, (a, b), c, correct, wrong, why) in enumerate(ANALOGY_SETS[test], start=1):
            # check: 4 distinct wrong options; the question doesn't repeat an L3 (or earlier) pair or answer pair
            assert len(wrong) == 4 and correct not in wrong and relation in RELATION_TEXT, (test, n)
            assert (a, b) not in old_pairs and (c, correct) not in old_pairs, (test, n)
            old_pairs |= {(a, b), (c, correct)}
            if {a, b, c, correct} & seen_words:
                REPORT.append(f"L{test}-Q{n:02d}: shares a word with an earlier analogy "
                              f"({', '.join(sorted({a, b, c, correct} & seen_words))}), different pair")
            seen_words |= {a, b, c, correct}
            letter = letters[n - 1]
            questions.append({
                "id": f"L{test}-Q{n:02d}",
                "text": f"{a} : {b}  =  {c} : ?",
                "options": arrange(correct, wrong, letter, rng),
                "answer": letter,
                "explanation": f"Relation: {relation} ({RELATION_TEXT[relation]}). {a} → {b}, so {c} → {correct}. "
                               + why,
                "source": "generated",
                "difficulty": difficulty,
                "relation": relation,
            })
        check_set(f"L{test}", questions, level)
        write_test(test, questions)


# ---------------------------------------------------------------- L15, L16 syllogisms (format of L4)
# Convention (the same as L4's checker): every group named in a question has at least one member
# ("existential import"), so "All A are B" implies "Some A are B". "Some" means at least one, possibly all.
# "It is not true that all A are B" (not_all) means the same as "Some A are not B"; two options that mean
# the same are never offered together (checked).

FORMS_NEW = {**FORMS, "not_all": "It is not true that all {x} are {y}."}


def holds_n(statement, regions):
    """Like holds(), for any number of terms; regions are bit masks of the terms an individual belongs to."""
    kind, x, y = statement
    if kind == "not_all":
        kind = "some_not"
    return holds((kind, x, y), regions)


def arrangements(n_terms):
    """Every way the groups can overlap: a set of non-empty Venn regions, with no group empty."""
    region_ids = range(1, 2 ** n_terms)
    for bits in range(1, 2 ** (2 ** n_terms - 1)):
        regions = [r for i, r in enumerate(region_ids) if bits >> i & 1]
        if all(any(r >> t & 1 for r in regions) for t in range(n_terms)):
            yield regions


_ARRANGEMENTS = {}


def must_follow(premises, conclusion, n_terms):
    """True if the conclusion holds in every arrangement where all premises hold (brute force)."""
    if n_terms not in _ARRANGEMENTS:
        _ARRANGEMENTS[n_terms] = list(arrangements(n_terms))
    models = [r for r in _ARRANGEMENTS[n_terms] if all(holds_n(p, r) for p in premises)]
    assert models, f"premises contradict each other: {premises}"
    return all(holds_n(conclusion, r) for r in models)


def same_meaning(s, t, n_terms):
    """True if the two statements are true in exactly the same arrangements."""
    return all(holds_n(s, r) == holds_n(t, r) for r in _ARRANGEMENTS[n_terms])


def sentence(statement, terms):
    kind, x, y = statement
    s = FORMS_NEW[kind].format(x=terms[x], y=terms[y])
    return s[0].upper() + s[1:]


def parse(statement):
    kind, x, y = statement.split()
    return kind, int(x), int(y)


# (difficulty, terms, premises, key conclusion or None for "none follows", [wrong conclusions], explanation)
# As in L4, options A–D are conclusions and E is "None of these conclusions follows": a question with a key
# has 3 wrong conclusions, a "none follows" question has 4.
# Statements are "kind x y" with kind all / no / some / some_not / not_all and x, y indexes into terms.
SYLLOGISM_SETS = {
    15: [
        ("easy", ["interns", "students", "library members"], ["all 0 1", "all 1 2"], "all 0 2",
         ["all 2 0", "some_not 2 0", "no 0 2"],
         "Interns are inside students, and students are inside library members, so every intern is a library "
         "member. The reverse ('all library members are …') doesn't follow: there may be library members who "
         "aren't students."),
        ("easy", ["pilots", "captains", "smokers"], ["no 0 2", "all 1 0"], "no 1 2",
         ["all 0 1", "some 2 1", "some_not 0 1"],
         "Every captain is a pilot and no pilot is a smoker, so no captain is a smoker. Whether some pilots "
         "aren't captains isn't stated: all pilots could be captains."),
        ("easy", ["cyclists", "helmet owners", "teachers"], ["all 0 1", "some 2 0"], "some 2 1",
         ["all 2 1", "some_not 2 1", "all 1 0"],
         "The teachers who are cyclists are also helmet owners, so some teachers are helmet owners. We know "
         "nothing about the other teachers, so 'all teachers' and 'some teachers are not' don't follow."),
        ("easy", ["doctors", "runners", "vegetarians"], ["some 0 1", "some 1 2"], None,
         ["some 0 2", "no 0 2", "some_not 2 0", "not_all 1 0"],
         "None follows. The runners who are doctors and the runners who are vegetarians may be different "
         "people or the same people, so 'some doctors are vegetarians' and 'no doctors are vegetarians' can "
         "each be false. Every runner could also be a doctor, so 'it is not true that all runners are doctors' "
         "doesn't follow either."),
        ("easy", ["volunteers", "paid staff", "organisers"], ["no 0 1", "some 2 0"], "some_not 2 1",
         ["no 2 1", "some_not 1 2", "some 2 1"],
         "The organisers who are volunteers can't be paid staff, so some organisers are not paid staff. The "
         "other organisers may or may not be paid staff, so 'no organisers are paid staff' doesn't follow."),
        ("medium", ["sprinters", "athletes", "chess players"], ["all 0 1", "no 2 1"], "no 0 2",
         ["some 1 2", "all 1 0", "some_not 1 0"],
         "Every sprinter is an athlete and no chess player is an athlete, so no sprinter is a chess player. "
         "'Some athletes are not sprinters' doesn't follow: all athletes could be sprinters."),
        ("medium", ["managers", "graduates", "team leaders"], ["all 0 1", "some_not 2 1"], "some_not 2 0",
         ["some_not 0 2", "no 2 0", "some_not 1 0"],
         "The team leaders who aren't graduates can't be managers (every manager is a graduate), so some team "
         "leaders are not managers. It could still be that every manager is a team leader."),
        ("medium", ["engineers", "problem solvers", "artists"], ["all 0 1", "no 2 0"], None,
         ["no 2 1", "some 2 1", "all 1 0", "some_not 2 1"],
         "None follows. Artists are outside the engineers, but that says nothing about whether they are "
         "problem solvers: 'no artists are problem solvers' and 'some artists are problem solvers' can each be "
         "false."),
        ("medium", ["volunteers", "retirees", "first-aiders"], ["some 0 1", "all 0 2"], "some 1 2",
         ["all 1 2", "some_not 1 2", "no 1 2"],
         "The retirees who are volunteers are first-aiders (every volunteer is), so some retirees are "
         "first-aiders. Nothing is said about the other retirees."),
        ("medium", ["smokers", "marathon runners", "club members"], ["no 0 1", "some 2 1"], "some_not 2 0",
         ["no 2 0", "some 0 2", "some_not 0 2"],
         "The club members who are marathon runners can't be smokers, so some club members are not smokers. "
         "Other club members could be smokers, so 'no club members are smokers' doesn't follow."),
        ("medium", ["contracts", "signed documents", "drafts"], ["all 0 1", "no 1 2"], "no 2 0",
         ["some 0 2", "some_not 1 0", "all 1 0"],
         "Every contract is signed and no signed document is a draft, so no draft is a contract. "
         "'Some signed documents are not contracts' doesn't follow: every signed document could be a contract."),
        ("medium", ["freelancers", "pension members", "part-timers"], ["no 0 1", "no 1 2"], None,
         ["no 0 2", "some 0 2", "all 0 2", "some_not 2 0"],
         "None follows. Two 'no' statements only say that freelancers and part-timers are both outside pension "
         "members; they may overlap completely, partly or not at all."),
        ("hard", ["nurses", "shift workers", "first-aiders"], ["all 0 1", "all 0 2"], "some 1 2",
         ["all 1 2", "no 1 2", "some_not 2 1"],
         "The nurses are both shift workers and first-aiders, and there is at least one nurse, so some shift "
         "workers are first-aiders. 'All shift workers are first-aiders' goes too far: there may be shift "
         "workers who aren't nurses."),
        ("hard", ["apprentices", "mentees", "workshop attendees", "remote workers"],
         ["all 0 1", "all 1 2", "no 2 3"], "no 0 3",
         ["some 3 1", "all 2 0", "some_not 2 0"],
         "Apprentices are inside mentees, mentees are inside workshop attendees, and no workshop attendee is a "
         "remote worker, so no apprentice is a remote worker. The reverse inclusions don't follow."),
        ("hard", ["suppliers", "exporters", "registered traders", "tax-exempt businesses"],
         ["some 0 1", "all 1 2", "no 2 3"], "some_not 0 3",
         ["no 0 3", "some 1 3", "some_not 3 0"],
         "The suppliers who are exporters are registered traders, so they can't be tax-exempt: some suppliers "
         "are not tax-exempt businesses. Other suppliers might be tax-exempt, so 'no suppliers are tax-exempt "
         "businesses' doesn't follow."),
    ],
    16: [
        ("easy", ["violinists", "musicians", "tone-deaf people"], ["all 0 1", "no 1 2"], "no 0 2",
         ["all 1 0", "some 2 0", "some_not 0 1"],
         "Every violinist is a musician and no musician is tone-deaf, so no violinist is tone-deaf. "
         "'All musicians are violinists' reverses the first statement."),
        ("easy", ["lawyers", "graduates", "partners"], ["all 0 1", "some 0 2"], "some 2 1",
         ["all 2 1", "all 1 0", "some_not 1 2"],
         "The lawyers who are partners are also graduates (every lawyer is), so some partners are graduates. "
         "The partners who aren't lawyers may or may not be graduates."),
        ("easy", ["laptops", "encrypted devices", "phones"], ["some_not 0 1", "some 1 2"], None,
         ["some 0 2", "no 0 2", "some_not 2 0", "all 1 0"],
         "None follows. The statements link laptops and phones only through encrypted devices, and in "
         "different ways ('some are not' and 'some are'), so laptops and phones may or may not overlap."),
        ("easy", ["reptiles", "warm-blooded animals", "mammals"], ["no 0 1", "all 2 1"], "no 2 0",
         ["some 2 0", "all 1 2", "some 1 0"],
         "Every mammal is warm-blooded and no reptile is, so no mammal is a reptile. 'All warm-blooded "
         "animals are mammals' reverses the second statement."),
        ("medium", ["auditors", "accountants", "graduates"], ["some_not 0 1", "all 0 2"], "some_not 2 1",
         ["some_not 1 2", "no 2 1", "some_not 0 2"],
         "The auditors who aren't accountants are graduates (every auditor is), so some graduates are not "
         "accountants. Other graduates could be accountants, so 'no graduates are accountants' doesn't follow."),
        ("medium", ["full-time staff", "freelancers", "invoice senders"], ["no 0 1", "all 1 2"], "some_not 2 0",
         ["no 2 0", "some 0 2", "some_not 0 2"],
         "There is at least one freelancer; every freelancer sends invoices and none is full-time, so some "
         "invoice senders are not full-time staff. Full-time staff could also send invoices, so 'no invoice "
         "senders are full-time staff' doesn't follow."),
        ("medium", ["temporary workers", "union members", "drivers"], ["no 0 1", "some_not 2 1"], None,
         ["some 2 0", "no 2 0", "some_not 2 0", "all 1 2"],
         "None follows. Both temporary workers and some drivers are outside the union, but that doesn't "
         "tell us whether any driver is a temporary worker: they may overlap or not."),
        ("medium", ["interns", "trainees", "badge holders"], ["all 0 1", "all 1 2"], "some 2 0",
         ["all 2 0", "no 0 2", "some_not 2 1"],
         "Interns are inside trainees, which are inside badge holders, and there is at least one intern, so "
         "some badge holders are interns. 'All badge holders are interns' reverses the direction."),
        ("medium", ["night-shift workers", "office-based staff", "security staff"], ["no 0 1", "all 0 2"],
         "some_not 2 1",
         ["no 2 1", "all 1 2", "some_not 1 2"],
         "There is at least one night-shift worker; each is security staff and none is office-based, so some "
         "security staff are not office-based. Other security staff could be office-based."),
        ("medium", ["pilots", "licence holders", "instructors", "trainees"],
         ["all 0 1", "some 2 0", "no 1 3"], "some_not 2 3",
         ["no 2 3", "some 2 3", "some_not 3 2"],
         "The instructors who are pilots are licence holders, so they can't be trainees: some instructors are "
         "not trainees. The other instructors might be trainees."),
        ("medium", ["editors", "writers", "poets", "readers"],
         ["all 0 1", "some 1 2", "all 2 3"], None,
         ["some 0 2", "some 0 3", "no 0 3", "not_all 3 1"],
         "None follows. The writers who are poets need not include any editor, so nothing links editors to "
         "poets or readers: 'some editors are readers' and 'no editors are readers' can each be false. All "
         "readers could be writers (for example if every reader is a poet), so the 'it is not true' option "
         "doesn't follow either."),
        ("medium", ["award winners", "designers", "portfolio owners"], ["some 0 1", "all 1 2"], "some 2 0",
         ["all 2 1", "some_not 0 2", "no 0 2"],
         "The award winners who are designers own portfolios (every designer does), so some portfolio owners "
         "are award winners. Nothing is said about the other award winners."),
        ("hard", ["shortlisted candidates", "late applicants", "interviewed candidates", "hired candidates"],
         ["no 0 1", "all 2 0", "all 3 2"], "no 3 1",
         ["some 1 0", "some_not 0 3", "all 2 3"],
         "Hired candidates are inside interviewed candidates, which are inside shortlisted candidates, and no "
         "shortlisted candidate applied late, so no hired candidate is a late applicant. It could be that every "
         "shortlisted candidate was hired, so 'some shortlisted candidates are not hired' doesn't follow."),
        ("hard", ["consultants", "graduates", "managers", "directors"],
         ["all 0 1", "no 2 0", "all 3 2"], "no 3 0",
         ["no 3 1", "some_not 3 1", "all 1 0"],
         "Directors are inside managers, and no manager is a consultant, so no director is a consultant. "
         "Nothing links directors to graduates: they may or may not be graduates."),
        ("hard", ["trainees", "managers", "employees", "ID-card holders"],
         ["no 0 1", "all 0 2", "all 2 3"], "not_all 3 1",
         ["no 3 1", "not_all 3 2", "some 1 0"],
         "There is at least one trainee; every trainee is an employee and so an ID-card holder, and no trainee "
         "is a manager. So at least one ID-card holder is not a manager: it is not true that all ID-card "
         "holders are managers. 'No ID-card holders are managers' goes too far, and every ID-card holder "
         "could be an employee."),
    ],
}


def build_new_syllogisms():
    old = {q["text"].split(" Assuming")[0].removeprefix("Statements: ")
           for q in json.loads((DATA / "logic-4.json").read_text(encoding="utf-8"))["questions"]}
    for level, test in enumerate(NEW_SETS["syllogisms"]):
        rng = random.Random(1500 + test)
        key_letters = balanced_letters(rng, 12, "ABCD")
        questions, keys = [], []
        for n, (difficulty, terms, premises, key, wrong, explanation) in enumerate(SYLLOGISM_SETS[test], start=1):
            qid = f"L{test}-Q{n:02d}"
            k = len(terms)
            premises = [parse(p) for p in premises]
            wrong = [parse(w) for w in wrong]
            assert len(wrong) == (3 if key else 4), f"{qid}: {len(wrong)} wrong conclusions"
            candidates = ([parse(key)] if key else []) + wrong
            text = lambda s: sentence(s, terms)
            # check: the key must follow; every wrong option must not (brute force over every arrangement)
            follows = [must_follow(premises, c, k) for c in candidates]
            if key:
                assert follows[0], f"{qid}: the key doesn't follow"
            bad = [text(w) for w in wrong if must_follow(premises, w, k)]
            assert not bad, f"{qid}: wrong option(s) also follow: {bad}"
            # check: no two options mean the same, and no option just repeats a premise
            for s, t in itertools.combinations(candidates, 2):
                assert not same_meaning(s, t, k), f"{qid}: '{text(s)}' and '{text(t)}' mean the same"
            assert not any(c in premises for c in candidates), f"{qid}: an option repeats a statement"
            premise_text = " ".join(text(p) for p in premises)
            assert premise_text not in old, f"{qid}: same statements as an L4 question"
            old.add(premise_text)
            if key:
                letter = key_letters.pop()
                options = arrange(text(parse(key)), [text(w) for w in wrong], letter, rng)
                keys.append(parse(key)[0])
            else:
                letter = "E"
                shuffled = [text(w) for w in wrong]
                rng.shuffle(shuffled)
                options = {LETTERS[i]: v for i, v in enumerate(shuffled)}
            options["E"] = "None of these conclusions follows."
            # the "must follow" tick for the "none" answer: no option A–D follows
            assert (letter == "E") == (not any(follows)), qid
            questions.append({
                "id": qid,
                "text": "Statements: " + premise_text + " Assuming the statements are true, which conclusion must "
                                                       "follow?",
                "options": options,
                "answer": letter,
                "explanation": explanation,
                "source": "generated",
                "difficulty": difficulty,
            })
        assert not key_letters
        # check: the key's form isn't predictable (no quantifier is the answer in more than half the questions)
        forms = {f: keys.count(f) for f in sorted(set(keys))}
        assert max(forms.values()) <= len(keys) // 2, (test, forms)
        premises3 = sum(len(s[2]) == 3 for s in SYLLOGISM_SETS[test])
        REPORT.append(f"L{test}: key forms {forms}, 'none follows' {sum(s[3] is None for s in SYLLOGISM_SETS[test])}, "
                      f"3-statement questions {premises3}")
        check_set(f"L{test}", questions, level)
        write_test(test, questions)


def build_new_sets():
    build_new_sequences()
    build_new_analogies()
    build_new_syllogisms()
    print("\n".join(REPORT))


if __name__ == "__main__":
    build_sequences()
    build_patterns()
    build_analogies()
    build_syllogisms()
    build_new_sets()
