"""Sanity-check the structure of every test JSON in site/data.

Run:  python tools/check_data.py
"""
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
SOURCES = {"recomputed", "dropped"}
FLAGS = {"recomputed", "dropped", "disputed", "missing-key", "truncated"}
TIME_LIMIT = {"numerical": 1020, "verbal": 480, "english": 900, "technical": 1200,
              "logic": {1: 600, 2: 720, 3: 480, 4: 720}}  # Logic: per subtest
OPTION_COUNT = {"numerical": 5, "verbal": 3, "english": 4, "logic": 5, "technical": 4}
# PwC entrance-test papers: 15 questions in 15 minutes, 4 options (verbal V8 also has 3-option True/False/Cannot say
# questions), and N6's data-interpretation questions use a passage instead of a chart.
ENTRANCE = {"V8": {"timeLimitSec": 900, "extraOptionCount": 4}, "N6": {"timeLimitSec": 900, "optionCount": 4}}
GENERATED = {"english", "logic", "technical"}  # sections written for the site, not from the PDF
# Tests imported from an outside question set (source "imported", key from that source). They are image-only:
# every question is a picture with the options drawn in it, so an explanation is optional (empty when the rule
# is unclear, see REVIEW.md). Their timer lives in site/js/data.js (SECTIONS.<section>.testMinutes), not in the JSON.
IMPORTED = {"L5": {"optionCounts": {5, 6}, "questions": 17}}
VERBAL_OPTIONS = {"A": "True", "B": "False", "C": "Cannot say"}
CUT_MARKER = "[...text cut off in source]"


def effective_answer(q):
    """The answer the site scores against (None = not scored)."""
    return q["verifiedAnswer"] if "verifiedAnswer" in q else q.get("answer")


def extra_option_count(test):
    """Verbal tests may only deviate from True / False / Cannot say if they are entrance-test papers."""
    return ENTRANCE.get(test["id"], {}).get("extraOptionCount")


def check_passages(test, say):
    passages = test.get("passages", {})
    for key, p in passages.items():
        text = p["text"].strip()
        if p["truncated"] != text.endswith(CUT_MARKER):
            say(f"passage {key}: 'truncated' is {p['truncated']} but the cut-off marker "
                f"is {'present' if text.endswith(CUT_MARKER) else 'missing'}")
        if not any(q.get("passage") == key for q in test["questions"]):
            say(f"passage {key}: not used by any question")
    for q in test["questions"]:
        if test["section"] == "verbal" and q["options"] != VERBAL_OPTIONS and len(q["options"]) != extra_option_count(test):
            say(f"{q['id']}: options are not True / False / Cannot say")
        flag = q.get("flag") or {}
        if flag.get("type") == "truncated" and not passages.get(q.get("passage"), {}).get("truncated"):
            say(f"{q['id']}: flagged truncated but its passage isn't")
        if q.get("answer") is None and flag.get("type") != "missing-key":
            say(f"{q['id']}: no PDF key but not flagged missing-key")


def check_test(path):
    test = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    say = problems.append

    section = test["section"]
    imported = IMPORTED.get(test["id"])
    if imported:
        if "timeLimitSec" in test:
            say("imported test: the timer belongs in data.js testMinutes, not timeLimitSec")
        if len(test["questions"]) != imported["questions"]:
            say(f"{len(test['questions'])} questions, expected {imported['questions']}")
    else:
        expected = TIME_LIMIT[section][test["test"]] if section == "logic" else TIME_LIMIT[section]
        expected = ENTRANCE.get(test["id"], {}).get("timeLimitSec", expected)
        if test.get("timeLimitSec") != expected:
            say(f"timeLimitSec is {test.get('timeLimitSec')}, expected {expected}")
    check_passages(test, say)

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
        # numerical needs a chart/table, verbal a passage; English passages are optional; others have none
        # (entrance-test numerical questions are plain sums, or use a passage instead of a chart)
        if section == "numerical" and test["id"] not in ENTRANCE and q.get("dataset") not in test.get("datasets", {}):
            say(f"{qid}: unknown dataset {q.get('dataset')!r}")
        if (section == "verbal" or "passage" in q) and q.get("passage") not in test.get("passages", {}):
            say(f"{qid}: unknown passage {q.get('passage')!r}")
        expected_counts = {ENTRANCE.get(test["id"], {}).get("optionCount", OPTION_COUNT[section]),
                           extra_option_count(test) or OPTION_COUNT[section]}
        if imported:
            expected_counts = imported["optionCounts"]
            if list(q["options"]) != list("ABCDEF"[:len(q["options"])]):
                say(f"{qid}: options must be lettered A, B, C… in order (the letters are printed in the image)")
        if len(q["options"]) not in expected_counts:
            say(f"{qid}: {len(q['options'])} options, expected {' or '.join(map(str, sorted(expected_counts)))}")
        if len(set(q["options"].values())) != len(q["options"]) or not all(str(v).strip() for v in q["options"].values()):
            say(f"{qid}: options are empty or repeated")
        if q.get("image") and not (SITE / q["image"]).exists():
            say(f"{qid}: image {q['image']} missing")
        if imported:
            if q.get("source") != "imported":
                say(f"{qid}: imported test but source is {q.get('source')!r}")
            if not q.get("image"):
                say(f"{qid}: imported (image-only) question has no image")
            if not isinstance(q.get("explanation"), str):
                say(f"{qid}: explanation must be a string (empty when the rule is unclear)")
        elif section in GENERATED:
            if q.get("source") != "generated":
                say(f"{qid}: generated section but source is {q.get('source')!r}")
            if not q.get("explanation"):
                say(f"{qid}: no explanation")
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
        if "acceptedAnswers" in q:
            acc = q["acceptedAnswers"]
            if not isinstance(acc, list) or len(acc) < 2 or len(set(acc)) != len(acc) \
                    or any(a not in q["options"] for a in acc):
                say(f"{qid}: acceptedAnswers {acc!r} must list 2+ distinct options")
            elif effective_answer(q) not in acc:
                say(f"{qid}: acceptedAnswers {acc!r} doesn't include the scored answer {effective_answer(q)!r}")
            if not q.get("flag"):
                say(f"{qid}: acceptedAnswers set but no flag note")
        if q.get("flag") and q["flag"]["type"] not in FLAGS:
            say(f"{qid}: bad flag type {q['flag']['type']!r}")
        if q.get("flag") is None and "answerSource" in q:
            say(f"{qid}: answerSource set but no flag note")
    return test, problems


def main():
    total = {s: 0 for s in OPTION_COUNT}
    scored = {s: 0 for s in OPTION_COUNT}
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
    print()
    for section in total:
        print(f"{section.capitalize():<10} {total[section]:>3} questions, {scored[section]} scored")


if __name__ == "__main__":
    main()
