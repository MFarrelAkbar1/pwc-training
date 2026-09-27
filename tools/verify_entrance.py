"""Recompute the entrance-test papers (Numerical N6, Verbal V8 word swaps) and compare with the JSON.

N6: each check is a small formula that returns an option letter. The answer the site scores against
(verifiedAnswer, else the PDF key) must equal it.
V8-Q01..Q05: the sentence is unswapped with every option; exactly one option must restore the corrected sentence.
Run:  python tools/verify_entrance.py
"""
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "site" / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def used(q):
    return q["verifiedAnswer"] if "verifiedAnswer" in q else q["answer"]


def nearest(value, q):
    """Letter of the option closest to value (options are plain numbers, with optional %, m, cm, commas or 1/n)."""
    def num(text):
        text = text.replace(",", "").rstrip("%").replace("cm", "").replace("m", "")
        if "/" in text:
            a, b = text.split("/")
            return int(a) / int(b)
        return float(text)
    numeric = {k: v for k, v in q["options"].items() if v != "Cannot tell"}  # 'Cannot tell' is never the nearest
    return min(numeric, key=lambda k: abs(num(numeric[k]) - value))


def text_option(text, q):
    return next((k for k, v in q["options"].items() if v == text), "none")


def band(value, q):
    """Letter of the range option ('Under 200,000', 'Between 200,000 and 220,000', 'Over 300,000') holding value."""
    for letter, text in q["options"].items():
        digits = [int(t.replace(",", "")) for t in text.replace("and", " ").split() if t.replace(",", "").isdigit()]
        if text.startswith("Under") and value < digits[0]:
            return letter
        if text.startswith("Between") and digits[0] <= value <= digits[1]:
            return letter
        if text.startswith("Over") and value > digits[0]:
            return letter
    return "none"


# ---- N6 passage figures ----
CENT_2008 = 9296
CENT_2007 = CENT_2008 - 1000  # "an increase of 1,000 on 2007"
WOMEN_PER_MAN = 7

CHECKS = {
    "N6-Q01": lambda q: nearest(125 ** (1 / 3), q),
    "N6-Q02": lambda q: band(sum(range(110, 631)), q),
    "N6-Q03": lambda q: nearest(sum(range(162, 727)) / len(range(162, 727)), q),
    "N6-Q04": lambda q: nearest(math.sqrt(8 ** 2 - 3 ** 2), q),
    "N6-Q05": lambda q: nearest((400 * 450) / (20 * 30), q),
    # Observed rate 21/50 applied to a further 100 tosses (verified answer, not the PDF key 63)
    "N6-Q06": lambda q: nearest(21 / 50 * 100, q),
    # +1 +1 +2 +2 +1 +1 +2: the differences repeat in pairs
    "N6-Q07": lambda q: nearest(22 + 2, q),
    "N6-Q08": lambda q: nearest((10 / 20) * (10 / 20), q),
    "N6-Q09": lambda q: nearest((102.0 - 100.5) / 100.5 * 100, q),
    "N6-Q10": lambda q: nearest(round(100 / 3), q),
    "N6-Q11": lambda q: nearest(100_000 / 16 - 100_000 / 50, q),
    "N6-Q12": lambda q: nearest(CENT_2007 * WOMEN_PER_MAN / (WOMEN_PER_MAN + 1) - CENT_2007 / (WOMEN_PER_MAN + 1), q),
    "N6-Q13": lambda q: text_option("Just over 12%" if 12 < (CENT_2008 - CENT_2007) / CENT_2007 * 100 < 12.1 else "?", q),
    "N6-Q14": lambda q: nearest(100_000 * 1.005 - 100_000, q),
    # 1-in-50 estimate applied to the 2008 centenarians (verified answer, not the PDF key 516,350)
    "N6-Q15": lambda q: nearest(CENT_2008 * 50, q),
}

# PDF keys (yellow highlights, letters E-H mapped back to A-D)
PDF_KEYS = {"N6-Q01": "C", "N6-Q02": "A", "N6-Q03": "A", "N6-Q04": "C", "N6-Q05": "C", "N6-Q06": "C", "N6-Q07": "B",
            "N6-Q08": "B", "N6-Q09": "B", "N6-Q10": "D", "N6-Q11": "D", "N6-Q12": "B", "N6-Q13": "A", "N6-Q14": "C",
            "N6-Q15": "A"}

# The sentences as they should read, one per word-swap question.
CORRECTED = [
    "Bound by the Alps to the north, the boot-shaped peninsula of mainland Italy stretches about 800km into the Mediterranean Sea.",
    "In the long fight for equal rights for black Americans Martin Luther King stands out for his great commitment to racial equality.",
    "Kites can be simple flat structures made from a framework of thin sticks covered with paper or more complex designs including data wings and aerofoils.",
    "Laws regulate government and state, the relationship between government and individuals and the conduct of individuals towards each other.",
    "Scientists use mathematics to test their theories, engineers use it to design new machines and entrepreneurs use it to manage their businesses.",
]


def check_numerical():
    bad = 0
    print("=== N6 ===")
    for q in load("numerical-6.json")["questions"]:
        got = CHECKS[q["id"]](q)
        scored = used(q)
        pdf = PDF_KEYS[q["id"]]
        ok = got == scored and q["answer"] == pdf
        bad += not ok
        note = f"  [PDF {q['answer']} -> used {scored}]" if scored != q["answer"] else ""
        print(f"{q['id']}  computed {got}  used {scored}  PDF key {q['answer']}  {'ok' if ok else 'MISMATCH'}{note}")
    return bad


def unswap(tokens, first, second):
    """All sentences you get by swapping an occurrence of `first` with a later occurrence of `second`.
    Trailing punctuation stays where it is (only the words move)."""
    words = [t.rstrip(",.") for t in tokens]
    tails = [t[len(w):] for t, w in zip(tokens, words)]
    idx1 = [i for i, w in enumerate(words) if w.lower() == first.lower()]
    idx2 = [i for i, w in enumerate(words) if w.lower() == second.lower()]
    results = []
    for i in idx1:
        for j in idx2:
            if i < j:
                w = list(words)
                w[i], w[j] = w[j], w[i]
                results.append(" ".join(a + b for a, b in zip(w, tails)))
    return results


def check_swaps():
    bad = 0
    print("\n=== V8 word swaps ===")
    for q, fixed in zip(load("verbal-8.json")["questions"][:5], CORRECTED):
        sentence = q["text"].split("“", 1)[1].rstrip("”")
        pairs = {k: tuple(w.strip() for w in v.split("/")) for k, v in q["options"].items()}
        right = [k for k, (a, b) in pairs.items() if fixed in unswap(sentence.split(), a, b)]
        # A wrong pair must also not appear in the sentence in the wrong order (the pair is given in sentence order).
        in_order = all(unswap(sentence.split(), a, b) for a, b in pairs.values())
        ok = right == [q["answer"]] and in_order
        bad += not ok
        print(f"{q['id']}  correct option(s) {right}  keyed {q['answer']}  {'ok' if ok else 'PROBLEM'}")
    return bad


if __name__ == "__main__":
    problems = check_numerical() + check_swaps()
    print("\nAll checks passed." if not problems else f"\n{problems} problem(s).")
