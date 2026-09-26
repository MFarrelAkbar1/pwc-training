"""Generate number-sequence questions (Logic subtest 1) with computed answers.

Each question comes from a rule (e.g. "differences grow by 2"). The rule produces
the whole sequence; the last term is hidden and becomes the answer. Distractors
are common slips (wrong difference, off by one, the previous rule step repeated).

Every question is checked before it is kept:
  - the rule really reproduces every shown term,
  - a simpler rule (constant difference or constant ratio) doesn't also fit the
    shown terms with a different next number,
  - the five options are distinct and exactly one equals the answer.

Usage:
  python tools/gen_sequences.py --samples 2      print a few questions
  (tools/gen_logic.py uses make_question to write site/data/logic-1.json)
"""
import argparse
import json
import random
import string

LETTERS = "ABCDE"


# ---------- rules: each returns (full sequence, one-line explanation) ----------

def arithmetic(rng):
    start, step = rng.randint(2, 40), rng.choice([-7, -6, -4, -3, 3, 4, 6, 7, 8, 9, 11, 12])
    seq = [start + step * i for i in range(7)]
    return seq, f"Add {step} each time: {seq[-2]} + {step} = {seq[-1]}." if step > 0 else \
        f"Subtract {-step} each time: {seq[-2]} − {-step} = {seq[-1]}."


def geometric(rng):
    start, ratio = rng.randint(2, 6), rng.choice([2, 3])
    seq = [start * ratio ** i for i in range(6)]
    return seq, f"Multiply by {ratio} each time: {seq[-2]} × {ratio} = {seq[-1]}."


def growing_difference(rng):
    start, first, grow = rng.randint(1, 20), rng.randint(1, 5), rng.choice([1, 2, 3])
    seq, diff = [start], first
    for _ in range(6):
        seq.append(seq[-1] + diff)
        diff += grow
    diffs = [b - a for a, b in zip(seq, seq[1:])]
    return seq, (f"The differences ({', '.join(map(str, diffs[:-1]))}) grow by {grow}, "
                 f"so the next difference is {diffs[-1]}: {seq[-2]} + {diffs[-1]} = {seq[-1]}.")


def alternating_ops(rng):
    start, add, mult = rng.randint(1, 6), rng.randint(2, 6), 2
    seq = [start]
    for i in range(6):
        seq.append(seq[-1] + add if i % 2 == 0 else seq[-1] * mult)
    last_op = f"+ {add}" if (len(seq) - 2) % 2 == 0 else f"× {mult}"
    return seq, f"Alternate '+{add}' and '×{mult}'. The last step is {last_op}: {seq[-2]} {last_op} = {seq[-1]}."


def interleaved(rng):
    a, da = rng.randint(1, 10), rng.choice([2, 3, 4, 5])
    b, db = rng.randint(20, 40), rng.choice([-2, -3, -4])
    seq = []
    for i in range(4):
        seq += [a + da * i, b + db * i]
    seq = seq[:7]  # hide the 7th term (the 4th term of the first series)
    return seq, (f"Two series alternate: {a}, {a + da}, {a + 2 * da}, … (+{da}) and "
                 f"{b}, {b + db}, {b + 2 * db}, … ({db}). The next term belongs to the first series: {seq[-1]}.")


def fibonacci_like(rng):
    x, y = rng.randint(1, 5), rng.randint(2, 7)
    seq = [x, y]
    while len(seq) < 7:
        seq.append(seq[-1] + seq[-2])
    return seq, f"Each term is the sum of the two before it: {seq[-3]} + {seq[-2]} = {seq[-1]}."


def squares_plus(rng):
    offset, first = rng.choice([-1, 1, 2, 3]), rng.randint(1, 4)
    seq = [n * n + offset for n in range(first, first + 6)]
    n = first + 5
    sign = f"+ {offset}" if offset > 0 else f"− {-offset}"
    return seq, f"Square numbers {sign}: {n}² {sign} = {seq[-1]}."


RULES = [arithmetic, geometric, growing_difference, alternating_ops, interleaved, fibonacci_like, squares_plus]


# ---------- checks ----------

def simpler_rule_disagrees(shown, answer):
    """True if a constant-difference or constant-ratio rule fits the shown terms but predicts differently."""
    diffs = {b - a for a, b in zip(shown, shown[1:])}
    if len(diffs) == 1 and shown[-1] + diffs.pop() != answer:
        return True
    if all(a != 0 for a in shown[:-1]):
        ratios = {b / a for a, b in zip(shown, shown[1:])}
        if len(ratios) == 1 and shown[-1] * ratios.pop() != answer:
            return True
    return False


def distractors(shown, answer, rng, rule_name=""):
    last_diff = shown[-1] - shown[-2]
    other_series_next = shown[-1] + (shown[-1] - shown[-3])  # continues the series the last shown term belongs to
    candidates = {
        shown[-1] + last_diff,          # repeats the last step
        answer + 1, answer - 1,         # off by one
        answer + 2, answer - 2,
        answer + (last_diff or 3),      # one step too far
        answer - (last_diff or 3),
        shown[-1] + (shown[-2] - shown[-3]),
    }
    candidates.discard(answer)
    pool = sorted(c for c in candidates if c > 0 or answer <= 0)
    rng.shuffle(pool)
    if rule_name == "interleaved" and other_series_next != answer:
        # the classic trap: continuing the wrong one of the two alternating series
        pool = [other_series_next] + [c for c in pool if c != other_series_next]
    return pool[:4]


def make_question(rng, number, rule=None, test_id="L1"):
    chosen_rule = rule
    while True:
        rule = chosen_rule or rng.choice(RULES)
        seq, explanation = rule(rng)
        shown, answer = seq[:-1], seq[-1]
        if simpler_rule_disagrees(shown, answer):
            continue
        wrong = distractors(shown, answer, rng, rule.__name__)
        if len(wrong) < 4:
            continue
        options = wrong + [answer]
        rng.shuffle(options)
        assert len(set(options)) == 5 and options.count(answer) == 1
        return {
            "id": f"{test_id}-Q{number:02d}",
            "text": "What number comes next?  " + ",  ".join(map(str, shown)) + ",  ?",
            "options": {LETTERS[i]: str(v) for i, v in enumerate(options)},
            "answer": LETTERS[options.index(answer)],
            "explanation": explanation,
            "source": "generated",
            "rule": rule.__name__,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=2)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    for n in range(1, args.samples + 1):
        print(json.dumps(make_question(rng, n), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
