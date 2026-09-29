"""Sanity-check the structure of every test JSON in site/data.

Run:  python tools/check_data.py
"""
import json
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
SOURCES = {"recomputed", "dropped"}
FLAGS = {"recomputed", "dropped", "disputed", "missing-key", "truncated", "ambiguous"}
TIME_LIMIT = {"numerical": 1020, "verbal": 480, "english": 900, "technical": 1200,
              "logic": {1: 600, 2: 720, 3: 480, 4: 720, 11: 600, 12: 600, 13: 480, 14: 480, 15: 720, 16: 720}}
# (Logic: per subtest)
OPTION_COUNT = {"numerical": 5, "verbal": 3, "english": 4, "logic": 5, "technical": 4}
# PwC entrance-test papers: 15 questions in 15 minutes, 4 options (verbal V8 also has 3-option True/False/Cannot say
# questions), and N6's data-interpretation questions use a passage instead of a chart.
ENTRANCE = {"V8": {"timeLimitSec": 900, "extraOptionCount": 4}, "N6": {"timeLimitSec": 900, "optionCount": 4}}
GENERATED = {"english", "logic", "technical"}  # sections written for the site, not from the PDF
# Tests imported from an outside question set (source "imported", key from that source). They are image-only:
# every question is a picture with the options drawn in it, so an explanation is optional (empty when the rule
# is unclear, see REVIEW.md). Their timer lives in site/js/data.js (SECTIONS.<section>.testMinutes), not in the JSON.
# L6–L9 come from the figural question bank PDF (tools/import_figural_bank.py): 4 options, 17 questions each.
# L10 comes from figural-tests.pdf (tools/import_figural_tests.py): 16 questions of mixed topics, 4 or 5 options,
# each with its topic.
IMPORTED = {"L5": {"optionCounts": {5, 6}, "questions": 17},
            **{f"L{n}": {"optionCounts": {4}, "questions": 17} for n in (6, 7, 8, 9)},
            "L10": {"optionCounts": {4, 5}, "questions": 16, "topics": {"analogy", "odd one out", "series"}}}
# English 4-6 each test one TOEFL ITP question type (tools/gen_english.py). Their timer lives in site/js/data.js
# (ENGLISH_MINUTES), not in the JSON. Each has a 6 / 10 / 4 easy / medium / hard mix and uses A-D five times each.
# Written Expression sentences mark their four underlined parts {A|…}…{D|…}; the options are those parts.
ENGLISH_TYPED = {"E4": "structure", "E5": "written expression", "E6": "reading"}
DIFFICULTY_MIX = {"easy": 6, "medium": 10, "hard": 4}
UNDERLINED_PART = re.compile(r"\{([A-F])\|([^}]*)\}")
PASSAGE_WORDS = (250, 350)
PASSAGE_QUESTIONS = (6, 7)
# Technical 4-8 (tools/gen_technical.py): 20 questions, a 6 / 10 / 4 easy / medium / hard mix in "level", A-D five
# times each, a topic on every question, and at least this share of scenario questions ("type").
TECHNICAL_TYPED = {"T4": 0.4, "T5": 0.4, "T6": 0.4, "T7": 0.4, "T8": 0.5}
# Length giveaway: the correct option may be the longest in at most a quarter of the questions, and lead every
# distractor by at most this many characters (options that are fixed names, e.g. COSO components, are exempt).
MAX_CORRECT_LEAD = 4
FIXED_NAME_OPTIONS = {"Information and communication"}
# Logic 11-16 (tools/gen_logic.py): second and third sets of number sequences (L11-12), analogies (L13-14) and
# syllogisms (L15-16). 15 questions, A-E three times each, and an easy / medium / hard mix; the second set of each
# topic has one easy question fewer. The timer is in both the JSON and data.js testMinutes, and they must agree.
LOGIC_TYPED = {"L11": "sequence", "L12": "sequence", "L13": "analogy", "L14": "analogy",
               "L15": "syllogism", "L16": "syllogism"}
LOGIC_MIX = {"L11": {"easy": 5, "medium": 7, "hard": 3}, "L13": {"easy": 5, "medium": 7, "hard": 3},
             "L15": {"easy": 5, "medium": 7, "hard": 3}, "L12": {"easy": 4, "medium": 8, "hard": 3},
             "L14": {"easy": 4, "medium": 8, "hard": 3}, "L16": {"easy": 4, "medium": 8, "hard": 3}}
LOGIC_RELATIONS = {"synonym", "antonym", "part-whole", "cause-effect", "effect-cause", "category-member",
                   "tool-user", "degree", "function", "sequence"}
NONE_FOLLOWS = "None of these conclusions follows."
MAX_LOGIC_LONGEST = 3  # the correct option may be the unique longest in at most 3 of 15 questions
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


def check_english_typed(test, skill, say):
    qs = test["questions"]
    if len(qs) != 20:
        say(f"{len(qs)} questions, expected 20")
    if "timeLimitSec" in test:
        say("typed English test: the timer belongs in data.js ENGLISH_MINUTES, not timeLimitSec")
    mix = {d: sum(q.get("difficulty") == d for q in qs) for d in DIFFICULTY_MIX}
    if mix != DIFFICULTY_MIX:
        say(f"difficulty mix {mix}, expected {DIFFICULTY_MIX}")
    letters = {letter: sum(q.get("answer") == letter for q in qs) for letter in "ABCD"}
    if set(letters.values()) != {len(qs) // 4}:
        say(f"answers {letters} aren't spread evenly over A-D")
    for q in qs:
        if q.get("skill") != skill:
            say(f"{q['id']}: skill {q.get('skill')!r}, expected {skill!r}")
        if not q.get("topic"):
            say(f"{q['id']}: no topic")
        marks = UNDERLINED_PART.findall(q["text"])
        if skill == "written expression":
            if [m[0] for m in marks] != list("ABCD"):
                say(f"{q['id']}: needs underlined parts {{A|…}} to {{D|…}} in order")
            elif dict(marks) != q["options"]:
                say(f"{q['id']}: options don't match the underlined parts")
        elif marks:
            say(f"{q['id']}: underlined-part marks outside a written-expression question")
        elif skill == "structure" and q["text"].count("______") != 1:
            say(f"{q['id']}: sentence needs exactly one blank")
    if skill == "reading":
        for key, p in test.get("passages", {}).items():
            words = len(p["text"].split())
            if not PASSAGE_WORDS[0] <= words <= PASSAGE_WORDS[1]:
                say(f"passage {key}: {words} words, expected {PASSAGE_WORDS[0]}-{PASSAGE_WORDS[1]}")
            used = sum(q.get("passage") == key for q in qs)
            if not PASSAGE_QUESTIONS[0] <= used <= PASSAGE_QUESTIONS[1]:
                say(f"passage {key}: {used} questions, expected {PASSAGE_QUESTIONS[0]}-{PASSAGE_QUESTIONS[1]}")
        if any("passage" not in q for q in qs):
            say("every reading question needs a passage")


def check_technical_typed(test, min_scenario, say):
    qs = test["questions"]
    if len(qs) != 20:
        say(f"{len(qs)} questions, expected 20")
    mix = {d: sum(q.get("level") == d for q in qs) for d in DIFFICULTY_MIX}
    if mix != DIFFICULTY_MIX:
        say(f"level mix {mix}, expected {DIFFICULTY_MIX}")
    letters = {letter: sum(q.get("answer") == letter for q in qs) for letter in "ABCD"}
    if set(letters.values()) != {len(qs) // 4}:
        say(f"answers {letters} aren't spread evenly over A-D")
    scenarios = sum(q.get("type") == "scenario" for q in qs)
    if scenarios < min_scenario * len(qs):
        say(f"{scenarios} scenario questions, expected at least {min_scenario:.0%}")
    longest = 0
    for q in qs:
        if q.get("type") not in ("scenario", "definition"):
            say(f"{q['id']}: type {q.get('type')!r}, expected scenario or definition")
        if not q.get("topic"):
            say(f"{q['id']}: no topic")
        correct = q["options"].get(q["answer"], "")
        lead = len(correct) - max(len(v) for k, v in q["options"].items() if k != q["answer"])
        longest += lead > 0
        if lead > MAX_CORRECT_LEAD and correct not in FIXED_NAME_OPTIONS:
            say(f"{q['id']}: correct option is {lead} characters longer than every distractor")
    if longest > len(qs) // 4:
        say(f"correct option is the longest in {longest} of {len(qs)} questions")


def check_logic_typed(test, kind, say):
    qs = test["questions"]
    if len(qs) != 15:
        say(f"{len(qs)} questions, expected 15")
    mix = {d: sum(q.get("difficulty") == d for q in qs) for d in ("easy", "medium", "hard")}
    if mix != LOGIC_MIX[test["id"]]:
        say(f"difficulty mix {mix}, expected {LOGIC_MIX[test['id']]}")
    letters = {letter: sum(q.get("answer") == letter for q in qs) for letter in "ABCDE"}
    if set(letters.values()) != {3}:
        say(f"answers {letters} aren't spread evenly over A-E")
    longest = 0
    for q in qs:
        lengths = [len(v) for v in q["options"].values()]
        correct = len(q["options"].get(q["answer"], ""))
        longest += correct == max(lengths) and lengths.count(correct) == 1
        if kind == "analogy" and q.get("relation") not in LOGIC_RELATIONS:
            say(f"{q['id']}: relation {q.get('relation')!r} not one of the known types")
        if kind == "syllogism" and q["options"].get("E") != NONE_FOLLOWS:
            say(f"{q['id']}: option E must be '{NONE_FOLLOWS}'")
        if kind == "sequence" and not re.match(r"What number (comes next|is missing)\?", q["text"]):
            say(f"{q['id']}: not a 'comes next' / 'is missing' question")
    if longest > MAX_LOGIC_LONGEST:
        say(f"correct option is the unique longest in {longest} of {len(qs)} questions")


def logic_timers_in_data_js():
    """Logic 1-4 and 11-16 have a timer in their JSON and in data.js testMinutes; the two must agree."""
    js = (SITE / "js" / "data.js").read_text(encoding="utf-8")
    block = re.search(r'prefix: "L".*?testMinutes: \{(.*?)\}', js, re.S)
    if not block:
        return ["data.js: Logic testMinutes missing"]
    minutes = {int(n): int(m) for n, m in re.findall(r"\b(\d+): (\d+)\b", block[1])}
    return [f"data.js: Logic subtest {n} is {minutes.get(n)} min, its JSON says {sec // 60}"
            for n, sec in TIME_LIMIT["logic"].items() if minutes.get(n) * 60 != sec]


def repeated_logic_questions():
    """Generated Logic questions (L1-L4, L11-L16) whose text appears more than once."""
    seen, problems = {}, []
    for n in [*range(1, 5), *range(11, 17)]:
        path = SITE / "data" / f"logic-{n}.json"
        if not path.exists():
            problems.append(f"{path.name} missing")
            continue
        for q in json.loads(path.read_text(encoding="utf-8"))["questions"]:
            key = (" ".join(q["text"].lower().split()), q.get("image"))  # L2 shares one text, differs by image
            if key in seen:
                problems.append(f"{q['id']}: same question as {seen[key]}")
            seen.setdefault(key, q["id"])
    return problems


def repeated_technical_questions():
    """Question texts that appear more than once across all Technical tests."""
    seen, problems = {}, []
    for path in sorted((SITE / "data").glob("technical-*.json")):
        for q in json.loads(path.read_text(encoding="utf-8"))["questions"]:
            key = " ".join(q["text"].lower().split())
            if key in seen:
                problems.append(f"{q['id']}: same question as {seen[key]}")
            seen.setdefault(key, q["id"])
    return problems


def english_timers_in_data_js():
    """The English 4-6 timers: ENGLISH_MINUTES defined in data.js and used for all three tests."""
    js = (SITE / "js" / "data.js").read_text(encoding="utf-8")
    minutes = re.search(r"const ENGLISH_MINUTES = \{([^}]*)\}", js)
    problems = []
    if not minutes:
        problems.append("data.js: ENGLISH_MINUTES missing")
    else:
        for key in ("structure", "writtenExpression", "reading"):
            if not re.search(rf"\b{key}: \d+", minutes[1]):
                problems.append(f"data.js: ENGLISH_MINUTES.{key} missing")
    for n, key in ((4, "structure"), (5, "writtenExpression"), (6, "reading")):
        if f"{n}: ENGLISH_MINUTES.{key}" not in js:
            problems.append(f"data.js: English test {n} doesn't use ENGLISH_MINUTES.{key}")
    return problems


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
    elif test["id"] in ENGLISH_TYPED:
        check_english_typed(test, ENGLISH_TYPED[test["id"]], say)
    else:
        if test["id"] in TECHNICAL_TYPED:
            check_technical_typed(test, TECHNICAL_TYPED[test["id"]], say)
        if test["id"] in LOGIC_TYPED:
            check_logic_typed(test, LOGIC_TYPED[test["id"]], say)
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
            if "topics" in imported and q.get("topic") not in imported["topics"]:
                say(f"{qid}: topic {q.get('topic')!r} not one of {sorted(imported['topics'])}")
            if (q.get("flag") or {}).get("type") == "ambiguous" and q.get("answerSource") != "dropped":
                say(f"{qid}: ambiguous question must be dropped (not scored)")
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
    timer_problems = english_timers_in_data_js()
    print(f"{'data.js':<18} English timers  {'ok' if not timer_problems else f'{len(timer_problems)} problem(s)'}")
    for p in timer_problems:
        print("   -", p)
    logic_timers = logic_timers_in_data_js()
    print(f"{'data.js':<18} Logic timers  {'ok' if not logic_timers else f'{len(logic_timers)} problem(s)'}")
    for p in logic_timers:
        print("   -", p)
    logic_repeats = repeated_logic_questions()
    print(f"{'logic-*':<18} repeated questions  {'none' if not logic_repeats else f'{len(logic_repeats)} problem(s)'}")
    for p in logic_repeats:
        print("   -", p)
    repeats = repeated_technical_questions()
    print(f"{'technical-*':<18} repeated questions  {'none' if not repeats else f'{len(repeats)} problem(s)'}")
    for p in repeats:
        print("   -", p)
    print()
    for section in total:
        print(f"{section.capitalize():<10} {total[section]:>3} questions, {scored[section]} scored")


if __name__ == "__main__":
    main()
