"""Sanity-check the structure of every test JSON in site/data.

Run:  python tools/check_data.py
"""
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
SOURCES = {"recomputed", "dropped"}
FLAGS = {"recomputed", "dropped", "disputed", "missing-key", "truncated"}
TIME_LIMIT = {"numerical": 1020, "verbal": 480}
VERBAL_OPTIONS = {"A": "True", "B": "False", "C": "Cannot say"}
CUT_MARKER = "[...text cut off in source]"


def effective_answer(q):
    """The answer the site scores against (None = not scored)."""
    return q["verifiedAnswer"] if "verifiedAnswer" in q else q.get("answer")


def check_verbal(test, say):
    passages = test.get("passages", {})
    for key, p in passages.items():
        text = p["text"].strip()
        if p["truncated"] != text.endswith(CUT_MARKER):
            say(f"passage {key}: 'truncated' is {p['truncated']} but the cut-off marker "
                f"is {'present' if text.endswith(CUT_MARKER) else 'missing'}")
        if not any(q["passage"] == key for q in test["questions"]):
            say(f"passage {key}: not used by any question")
    for q in test["questions"]:
        if q["options"] != VERBAL_OPTIONS:
            say(f"{q['id']}: options are not True / False / Cannot say")
        flag = q.get("flag") or {}
        if flag.get("type") == "truncated" and not passages.get(q["passage"], {}).get("truncated"):
            say(f"{q['id']}: flagged truncated but its passage isn't")
        if q.get("answer") is None and flag.get("type") != "missing-key":
            say(f"{q['id']}: no PDF key but not flagged missing-key")


def check_test(path):
    test = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    say = problems.append

    if test.get("timeLimitSec") != TIME_LIMIT[test["section"]]:
        say(f"timeLimitSec is {test.get('timeLimitSec')}, expected {TIME_LIMIT[test['section']]}")
    if test["section"] == "verbal":
        check_verbal(test, say)

    for key, ds in test.get("datasets", {}).items():
        if not (SITE / ds["image"]).exists():
            say(f"dataset {key}: image {ds['image']} missing")
        for b in ds["blocks"]:
            if b["kind"] == "table":
                bad = [r[0] for r in b["rows"] if len(r) != len(b["columns"])]
                if bad:
                    say(f"dataset {key}: rows with wrong length {bad}")
            else:
                bad = [s["name"] for s in b["series"] if len(s["values"]) != len(b["labels"])]
                if bad:
                    say(f"dataset {key}: series with wrong length {bad}")

    ids = set()
    for q in test["questions"]:
        qid = q["id"]
        if qid in ids:
            say(f"{qid}: duplicate id")
        ids.add(qid)
        if not qid.startswith(test["id"] + "-Q"):
            say(f"{qid}: id doesn't match test {test['id']}")
        ref = "dataset" if test["section"] == "numerical" else "passage"
        pool = test.get("datasets" if ref == "dataset" else "passages", {})
        if q.get(ref) not in pool:
            say(f"{qid}: unknown {ref} {q.get(ref)!r}")
        if q.get("answer") is not None and q["answer"] not in q["options"]:
            say(f"{qid}: answer {q['answer']!r} not an option")
        if "answerSource" in q:
            if q["answerSource"] not in SOURCES:
                say(f"{qid}: bad answerSource {q['answerSource']!r}")
            va = q.get("verifiedAnswer", "missing")
            if q["answerSource"] == "dropped" and va is not None:
                say(f"{qid}: dropped question should have verifiedAnswer null")
            if q["answerSource"] == "recomputed" and va not in q["options"]:
                say(f"{qid}: verifiedAnswer {va!r} not an option")
        if q.get("flag") and q["flag"]["type"] not in FLAGS:
            say(f"{qid}: bad flag type {q['flag']['type']!r}")
        if q.get("flag") is None and "answerSource" in q:
            say(f"{qid}: answerSource set but no flag note")
    return test, problems


def main():
    total = {"numerical": 0, "verbal": 0}
    scored = {"numerical": 0, "verbal": 0}
    for path in sorted((SITE / "data").glob("*.json")):
        test, problems = check_test(path)
        n = len(test["questions"])
        s = sum(1 for q in test["questions"] if effective_answer(q) is not None)
        total[test["section"]] += n
        scored[test["section"]] += s
        status = "ok" if not problems else f"{len(problems)} problem(s)"
        print(f"{path.name:<18} {n:>3} questions ({s} scored)  {status}")
        for p in problems:
            print("   -", p)
    print(f"\nNumerical: {total['numerical']} questions, {scored['numerical']} scored")
    print(f"Verbal:    {total['verbal']} questions, {scored['verbal']} scored")


if __name__ == "__main__":
    main()
