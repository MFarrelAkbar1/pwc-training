# Review: problems found in the source PDF

Nothing from the PDF is overwritten. Every question keeps the PDF key in `answer`.
When there's a problem, the question also gets:

| Field | Meaning |
|---|---|
| `verifiedAnswer` | The answer the site scores against (`null` = not scored) |
| `answerSource` | `"recomputed"` (my answer replaces the PDF key) or `"dropped"` (no option is correct) |
| `acceptedAnswers` | Optional list of letters that all count as correct (only when two options are equally right, e.g. N1-Q13). Must include the scored answer |
| `flag` | `{ type: "recomputed" \| "dropped" \| "disputed" \| "missing-key" \| "truncated", note }`, shown to you in the quiz |

**Rules for numerical (agreed):**
- My recomputed answer matches an option and differs from the key → **recomputed** (use mine, show note).
- No option is correct → **dropped** (shown in review, not scored).
- The question is ambiguous → **disputed** (keep PDF key, show note).

**Rules for verbal (agreed):**
- I disagree with the key → **disputed** (keep PDF key, give my answer in the note).
- The passage *clearly contradicts* the key → **recomputed** (use mine).
- No key in the PDF → **missing-key** (my answer is used).
- The statement depends on a passage that is cut off → **truncated** (keep PDF key).

Recheck any time with `python tools/verify_numerical.py` (answers) and `python tools/check_data.py` (structure).

**Status:** All 14 tests are checked. Numerical: 115 questions, 114 scored (N6 is the entrance-test paper, see below). Verbal: 119 questions (V4 has 14; V8 is the entrance-test paper), all scored.

## Numerical summary

| Question | PDF key | Used | Decision |
|---|---|---|---|
| N1-Q01 | B | **D** | recomputed |
| N1-Q02 | B | **D** | recomputed |
| N1-Q07 | C | **E** | recomputed |
| N1-Q13 | B | B **or C** | disputed, both accepted (verification pass) |
| N1-Q19 | B | — | dropped |
| N2-Q02 | E | **D** | recomputed |
| N2-Q07 | B | B | disputed |
| N2-Q11 | B | B | disputed (typo in question) |
| N2-Q17 | B | **A** | recomputed |
| N3-Q01 | C | C | disputed |
| N3-Q04 | B | **E** | disputed, uses E (your decision) |
| N3-Q08 | D | **E** | recomputed |

In total: 6 recomputed, 1 dropped (N1-Q19), 3 disputed with the PDF key kept, 1 disputed using my answer (N3-Q04), and 1 disputed where both B and C are accepted (N1-Q13). Tests 4 and 5 have no key problems.

For every question where the site uses my answer, the `explanation` shows the correct working, so it always matches the answer that's scored. The PDF's original working is kept at the end of the flag note ("PDF working: …").

---

## Numerical Test 1

| Question | PDF key | Used | Decision | Reasoning |
|---|---|---|---|---|
| N1-Q01 | B (32,000) | **D (64,000)** | recomputed | The chart shows Radio Advertising at **20% in 2003**; 10% is its 2004 bar. Total 2003 = 27,200 ÷ 8.5% = 320,000; 20% of that = 64,000. |
| N1-Q02 | B (52,500) | **D (56,000)** | recomputed | "100,000 in 2004, an increase of 25% from 2003" → 2003 = 100,000 ÷ 1.25 = **80,000** (the PDF used 75,000). Total 2003 = 320,000; Newspaper 17.5% = 56,000. |
| N1-Q07 | C (525) | **E (None of these)** | recomputed | The question asks for the *increase*: 525 − 300 = **225**, not an option. 525 is the new total. The PDF's own explanation says "implies a 225 increase". |
| N1-Q19 | B (24%) | not scored | dropped | The PDF's formula (142,034 − 41,175) ÷ 41,175 gives **245%**. No reading matches an option (Amber Hill ÷ Kinsop = 29%; difference ÷ Kinsop = 71%). |

Explanation slips, key still right (the site shows corrected working):
- **N1-Q04**: "0.15 × 46,000 = 69,000" should be 46,000 × 15/10 = 69,000.
- **N1-Q17**: the PDF uses 64,651 vehicles; the table says 64,561.

---

## Numerical Test 2

| Question | PDF key | Used | Decision | Reasoning |
|---|---|---|---|---|
| N2-Q02 | E (7.9%) | **D (6.8%)** | recomputed | "Average annual growth for 1999 and 2000" = average of 1999 growth (2,375 → 2,508 = 5.6%) and 2000 growth (2,508 → 2,709 = 8.0%) = **6.8%**. The PDF only computed 2000, and 201 ÷ 2,508 is 8.0%, not 7.9%. |
| N2-Q07 | B (31.31%) | B (31.31%) | disputed | Ambiguous. The PDF grows exploration by 8% too, then adds £100k: (0.29 × 4.32m + 0.1m) ÷ 4.32m = 31.31%. Reading it as 2008 exploration + £100k gives 1.26m ÷ 4.32m = **29.2%**, which matches no option exactly (closest is A, 29.7%). |
| N2-Q11 | B (4) | B (4) | disputed | The question says **5,800,000** vehicles, but the chart is in thousands and the PDF works with 58,000. With 58,000: 35 → 40.8 → 47.6 → 55.6 → 64.8, so **4 years**. Read literally, 5.8m would take ~33 years. Almost certainly a typo in the question. |
| N2-Q17 | B (3.3%) | **A (3%)** | recomputed | "Constant annual rate of growth" compounds: (16 ÷ 13.4)^(1/6) − 1 = **3.0%** (check: 13.4 × 1.03⁶ = 16.0). The PDF divided simple growth by 6, and 19.4% ÷ 6 = 3.2%, not 3.3%. |

Checked because you flagged them; **keys are correct** (only the explanations are sloppy):
- **N2-Q03**: the PDF writes 1.1m cars, then 4.1m, then 3.6m. The table says 4.1m. 90% × 4.1 = 3.69m cars; urban pop = 86.4% × 35.6 = 30.76m; 3.69 ÷ 30.76 = **12%** (D).
- **N2-Q12**: the PDF mixes units. Europe: 0.3bn passengers × 1,000 km = 300bn km → 0.9bn × 800 km = 720bn km = **+140%** (E).

Other explanation slips, key still right:
- **N2-Q09**: "(1 − 0.02) × 35,000" should be (1 − 0.2).

---

## Numerical Test 3

| Question | PDF key | Used | Decision | Reasoning |
|---|---|---|---|---|
| N3-Q01 | C (Korea) | C (Korea) | disputed | The chart shows only each drug's **percentage split** by region, not dollar totals, so "exceed (in $)" can't strictly be answered. But **no option is "Cannot say"**: all five are regions. The only reading that gives an answer is by share: Korea, where Parnol has 37% vs Tequental's 15%. |
| N3-Q04 | B (400,000 higher) | **E (Cannot say)** | disputed (your decision: use E) | Hire Purchase is 25% (Printing) + 50% (Design); the other departments are 0%. If each department spends an equal $400k, HP = $300k, and +20% = **$60,000 higher**, which isn't an option. The PDF contradicts itself: the working ends "40,000 higher" and the key says 400,000. The chart never says how the $2m is split between departments, so the effect can't be calculated: **Cannot say**. |
| N3-Q08 | D (2000) | **E (Cannot say)** | recomputed | The unemployment rate is a % of the **workforce**, and the workforce size isn't given (only population can be derived from GDP ÷ GDP per head). The PDF's own explanation concludes "Cannot say". |

Checked because you flagged them; **keys are correct**:
- **N3-Q02**: the chart shows Production Lease Purchase = 30%, and 30% × 575,000 = **172,500** (B). The explanation's "35/100" is a typo (35% would give 201,250).
- **N3-Q07**: Year 2 → 3 fell by a factor of 8.5 ÷ 10.6 = 0.802; Year 4 = 8.5 × 0.802 = **£6.8m** (D).

Other notes:
- **N3-Q18**: the explanation says "84% qualified" but uses 2,494 staff, which is 86% (100% − 14%). 86% is correct, and so is the key (D).
- **Machinery chart**: as printed, Printing's bars add up to **105%** (45 + 35 + 25). No answer depends on the total, so I transcribed it as printed and noted it on the chart.
- **N3-Q09**: the explanation writes 1.02 for a 20% rise (should be 1.2). The key is right.

---

## Numerical Test 4

**No key problems.** All 20 keys match the chart data. Slips in the PDF's working:
- **N4-Q11**: the last line of the working lists "Haydn & Lennon 75 / €650"; that should be **Brahms & Dylan**, which is key E.
- **N4-Q19**: the working writes a Tele-Fax discount total of 32,500; it's 45 × 700 = 31,500. The final saving of €21,240 is right.
- **N4-Q20**: the working gives Complaints 65.9% and Claims 48%. From the table they're 122/180 = **67.8%** and 48/120 = **40.0%**. Complaints is still highest, so key C holds. (I checked the full page: the table has only three rows.)

---

## Numerical Test 5

**No key problems.** All 20 keys match the chart data.
- **N5-Q16**: the question asks how much was *gambled*, but the chart gives casino *revenue*. The PDF treats them as the same, and I kept that. 140,000 ÷ 1,520,000 = £0.092 ≈ £0.09 (E).

---

## Verbal summary

I judged all 104 statements using only the passage. **I disagree with 12 keys** (10 disputed, 2 switched). V3-Q01 has no key, and V3-Q12 can't be checked because its passage is cut off. The table lists all 18 flagged statements, including 4 truncated ones where I agree with the key. "Confidence" is how sure I am of *my* answer.

| Question | PDF key | My answer | Used | Flag | Confidence |
|---|---|---|---|---|---|
| V1-Q13 | True | Cannot say | **Cannot say** | recomputed (your decision) | high |
| V2-Q02 | False | Cannot say | False | disputed | medium |
| V2-Q03 | True | Cannot say | **Cannot say** | recomputed (your decision) | high |
| V2-Q10 | Cannot say | Cannot say | Cannot say | truncated | — (agree) |
| V2-Q11 | Cannot say | True | **True** | recomputed (your decision); flag now **disputed** (verification pass) | medium |
| V2-Q13 | True | Cannot say | True | disputed | low |
| V2-Q15 | False | Cannot say | False | disputed | low |
| V3-Q01 | *none* | Cannot say | **Cannot say** | no key in source (my judgment, confirmed) | high |
| V3-Q07 | Cannot say | Cannot say | Cannot say | truncated | — (agree) |
| V3-Q09 | True | Cannot say | **Cannot say** | recomputed (your decision) | medium |
| V3-Q12 | True | Cannot say* | True | truncated | — (*from visible text only) |
| V4-Q05 | True | **False** | **False** | recomputed (confirmed); flag now **disputed** (verification pass) | high |
| V4-Q06 | False | **True** | **True** | recomputed (confirmed) | high |
| V4-Q09 | Cannot say | Cannot say | Cannot say | truncated | — (agree) |
| V4-Q15 | Cannot say | Cannot say | Cannot say | truncated | — (agree) |
| V6-Q14 | True | Cannot say | True | disputed | medium |
| V7-Q06 | Cannot say | True | **True** | recomputed (your decision) | low |
| V7-Q14 | False | Cannot say | False | disputed | medium |

**After your decisions:** 7 recomputed (the 2 switches plus 5 where you chose my answer), 5 disputed with the PDF key kept (V2-Q02, V2-Q13, V2-Q15, V6-Q14, V7-Q14), 1 with no key in source, and 5 truncated with the PDF key kept (V3-Q12 stays True).
Since the verification pass, V2-Q11 and V4-Q05 still use my answer (`answerSource: "recomputed"`), but their flag type is **disputed**, because another source disagrees (see "Verification pass vs Verified PDF").

Every verbal statement now has a one-line explanation that matches the answer the site uses. For the disputed ones, the explanation ends with "The source key was X; some readings differ."

---

## Verbal: details

### Switched: the passage clearly contradicts the key
- **V4-Q05**: "In Japan and Germany less than 60% of the population is under 65." The passage says the 65+ share there "is set to **rise to** 40%". So today it's below 40%, which means more than 60% are under 65. Even once it reaches 40%, exactly 60% would be under 65, not *less than* 60%. The statement is **False**; the PDF says True.
- **V4-Q06**: "Birth rate decreases are not restricted to developed countries." The passage says underdeveloped countries "have experienced **a much smaller decrease** in birth rates". A smaller decrease is still a decrease, so the statement is **True**; the PDF says False.

### No key in the PDF
- **V3-Q01**: "Some commentators believe the best way to boost a flagging economy would be… 'green'-related infrastructure projects." The commentators argue for *major infrastructure projects* in general. The green angle belongs to "many people", and nobody calls it "the best way". **Cannot say.**
- (V3-Q15's key is C, on the next page, as you found. It's in the JSON.)

### Disputed: my reasoning (you chose **my answer** for V1-Q13, V2-Q03, V2-Q11, V3-Q09 and V7-Q06; the rest keep the PDF key)
- **V1-Q13** (key True → mine Cannot say). The passage says forecasts depend on "the individual analyst's general approach, with some being bolder than others". It never connects boldness to *optimism*; optimism appears only as the usual direction of error.
- **V2-Q02** (key False → mine Cannot say). The passage says the law requires immediate threats to be cleaned up. It says nothing about how law (or litigation) treats long-term hazards, so we can't tell whether it "draws a distinction".
- **V2-Q03** (key True → mine Cannot say). "**Much of**" soil contamination isn't hazardous while undisturbed, so not all of it. And contaminated ground water is given as an immediate threat with no mention of disturbance. The statement "has to be disturbed before…" is too strong.
- **V2-Q11** (key Cannot say → mine True). Employees who rated their boss incompetent had 25% higher heart-disease risk, with external factors controlled. That's a stated link. The only argument for Cannot say is that the bosses were *rated* incompetent, not *shown* to be.
- **V2-Q13** (key True → mine Cannot say, low). The directors want high *funding*; "work flowing to national industries" is a consequence of funding, not something the passage says they want.
- **V2-Q15** (key False → mine Cannot say, low). Costs have risen (the budget almost doubled) and are met by "the participating countries", including Italy and Britain. Whether *only* Italy and Britain pay isn't stated either way.
- **V3-Q09** (key True → mine Cannot say). Only "some scientists *claim*" the long-range accuracy is unknowable. That's an opinion in the passage, not an established fact.
- **V6-Q14** (key True → mine Cannot say). The passage implies staff have passwords, but never says *all department managers* have *their own*.
- **V7-Q06** (key Cannot say → mine True, low). "Greater funding… **has in turn increased** the number of world class Irish athletes" is a direct causal claim, so without it there'd be fewer. The key's view is that counterfactuals are never strictly proven.
- **V7-Q14** (key False → mine Cannot say). Visitors cause only *some* of the pollution and *some* of the pests, and other causes remain. So damage would *probably* still have increased, but the passage doesn't quantify the causes.

### Looked at closely, as you asked
- **V1-Q13, V2-Q11, V4-Q05, V4-Q06, V6-Q14, V7-Q14**: all six are in the tables above. I switched two of them (V4-Q05 and V4-Q06) and disputed the other four.

---

## Verbal: source problems

**Cut-off passages** (six, not four). Each is transcribed exactly and ends with "[...text cut off in source]":

| Passage | Ends with | Statements flagged "truncated" |
|---|---|---|
| V2 p3: bosses & heart disease | "…managers should be given training to help them improve" | **V2-Q10** (asks what the training should improve) |
| V3 p3: climate scenarios | "…what, if anything, does that tell us about the next" | **V3-Q07** |
| V3 p4: earthquakes | "…the animals are reacting to chang" | **V3-Q12**: its "electromagnetic signals" never appear in the visible text, so the key can't be checked |
| V4 p2: ageing population | "…healthcare and education for the" | none (Q5 and Q6 don't depend on the missing end) |
| V4 p3: work stress | "…thirty percent of men said that the" | **V4-Q09** (a statistic about men) |
| V4 p5: U3b Networks | "…five satellites circling" | **V4-Q15** (satellite cost) |

**Other:**
- **V4-Q04** doesn't exist in the PDF, so Verbal 4 has **14 questions**. The JSON notes this and skips from Q03 to Q05.
- **V4-Q15** reads "?8m" in the PDF itself (the currency symbol is missing in the source image). I kept it as printed.
- The PDF's own typos are kept word for word (e.g. "to a large extend inherited", "its incidence vary", "pouring over books", "that that the animals").
- Two passages had scrambled word order in the PDF's text layer (V3 earthquakes, V5 smoke-free law). I transcribed those from the page images. Every other passage sentence and statement was machine-checked against the PDF text.

---

# PwC entrance test: Verbal V8 and Numerical N6

Source: `pdf-pwc-entrance-test-amp-answer_compress.pdf` (30 questions, then an answer section). The PDF is not committed.
The answer section relabels the options E–H; they are mapped back to A–D. The letter keys are **yellow highlights on the
page images**, not in the PDF's text, so they were read from the rendered pages (the numeracy and matching questions have no
"Answer:" line at all). The site numbers the tests V8 and N6; the PDF's question numbers are in the tables below.

| Test | Questions | Timer | Layout |
|---|---|---|---|
| V8 | 5 word swap, 5 True/False/Cannot say (acids passage), 5 matching | 15 min | The instructions or passage sit next to each group of questions |
| N6 | 10 numeracy, then 5 data interpretation (centenarians passage) | 15 min | Passage beside Q11–Q15; Q1–Q10 are single-column |

Both papers use 4 options (A–D). Both also join the section's mixed random set and the wrong-answer bank like any other test.
`python tools/verify_entrance.py` recomputes all 15 N6 answers and checks the V8 word-swap options; `python tools/check_data.py`
checks the structure.

## Decisions

| Question | PDF Q | PDF key | Used | Decision | Reasoning |
|---|---|---|---|---|---|
| V8-Q06 | 36 | B (False) | **C (Cannot say)** | recomputed (your decision) | The passage only says the stomach contains hydrochloric acid. It says nothing about how strong stomach acid is. |
| V8-Q12 | 42 | B (Sentences) | B | disputed (ambiguous relation) | Fire → smoke is "produces", but sentences are built from words (part–whole). Letters or Voices fit other readings. Key kept. |
| V8-Q14 | 44 | B (Interior) | B | disputed (ambiguous relation) | Fuzzy/Smooth as opposites gives Surface/Interior, but both words can describe a surface (Veneer, Appearance). Key kept. |
| N6-Q06 | 51 | C (63) | **A (42)** | recomputed, flagged **disputed** (your decision) | 21 heads in 50 tosses is 42%, so 42 in a further 100. 63 is 42% of 150 (all tosses), not of the further 100. A fair-coin argument gives 50, which isn't an option. |
| N6-Q15 | 60 | A (516,350; E in the PDF) | **B (464,800; F in the PDF)** | recomputed, flagged **disputed** (your decision) | 1 in 50 × 9,296 centenarians (2008) = 464,800. The PDF key can't be reproduced from the passage, and the PDF gives no working. |
| V8-Q04 | 34 | "Between and (the first) the" | between / the | corrected pair (your decision) | See below. |

The two "ambiguous relation" questions use the **disputed** flag type with a note that starts "Ambiguous relation."

All other keys are correct as printed. Recomputing the numeracy questions matched the PDF key every time except N6-Q06 and N6-Q15
above (`tools/verify_entrance.py`). Working: N6-Q02 sum = 521 × 370 = 192,770 (under 200,000); Q04 √55 = 7.4; Q05 180,000 ÷ 600 = 300;
Q09 1.5 ÷ 100.5 = 1.49%; Q11 6,250 − 2,000 = 4,250; Q12 8,296 × 6/8 = 6,222; Q13 1,000 ÷ 8,296 = 12.05%; Q14 100,500 − 100,000 = 500.

## Word-swap questions (V8-Q01 to Q05)

The PDF asks for the two words in a free-text box. On the site each question has 4 options, each a pair of words from the sentence
in the order they appear, with one correct pair and 3 plausible wrong pairs. `tools/verify_entrance.py` un-swaps every option and
checks that exactly one restores the corrected sentence.

- **V8-Q04 (PDF Q34).** The PDF's "(the first) the" is confusing. The corrected pair is **between** and the **the** just before "government":
  swapping them gives "the relationship between government and individuals". (That "the" is the only one that works; a swap can't
  add a second "the" before "government".)
- **V8-Q02 (PDF Q32).** "racial rights … equal equality" has two readings: swapping *rights* and *equality* also gives a grammatical
  sentence ("racial equality … equal rights"). The PDF key is *racial / equal*, and that pair is the only one offered, so the
  question still has exactly one correct option.
- The PDF's typos are kept in the sentences ("data wings" in Q33, "equal equality" in Q32).

## Explanations

The PDF's explanations were used for the matching and True/False questions and reworded where garbled ("we must only taste weak
solutions", "soluations", "It is be inferred"). V8-Q06's explanation is rewritten for Cannot say. The numeracy explanations
(the PDF has none) show the calculation.

---

# Generated sections: English, Logic, Technical

These 430 questions were **written for this site**, not taken from the PDF. Every one has
`"source": "generated"` and shows a "Generated · unverified" label. The section pages say that
the questions haven't been checked against an official source.

| Section | Tests | Questions | Timer | How answers were produced |
|---|---|---|---|---|
| English (TOEFL-style) | E1–E3 | 3 × 20 (8 sentence completion, 4 error spotting, 8 reading from 2 passages) | 15 min each | Written and checked by hand |
| English (TOEFL-style) | E4–E6 | 3 × 20: Structure, Written Expression, Reading (3 passages) | 13 / 13 / 25 min | Written by hand in `tools/gen_english.py`, blind-checked (see "English 4–6" below) |
| Logic (TPA-style) | L1–L4 | 4 × 15 | 10 / 12 / 8 / 12 min | **Computed** by `tools/gen_logic.py` (L1, L2, L4); L3 written by hand |
| Logic (TPA-style) | L11–L16 | 6 × 15: two more sets each of sequences, analogies, syllogisms | 10 / 10 / 8 / 8 / 12 / 12 min | Written in `tools/gen_logic.py`; sequences and syllogisms **checked in code**, all blind-checked (see "Logic Subtests 11–16" below) |
| Technical (Risk Assurance) | T1–T3 | 3 × 20 (18 of 60 scenario-based; easy, medium and hard mixed) | 20 min each | Written and checked by hand |
| Technical (Risk Assurance) | T4–T8 | 5 × 20 by topic + a mixed mock (58 of 100 scenario-based) | 20 min each | Written by hand in `tools/gen_technical.py`, facts checked against sources, blind-checked (see "Technical 4–8" below) |

Regenerate the Logic tests with `python tools/gen_logic.py` (seeded, so the output is the same each time).
`python tools/check_data.py` checks the structure of every test file in `site/data`.

## Least sure: please review these

### English
| Question | Issue |
|---|---|
| **Format** | Follows TOEFL ITP / paper-based style (structure, error spotting, reading). The current TOEFL iBT has no grammar section, so this matches the older format. |
| E1-Q06 | "Of the two candidates … the **more** qualified": a strict grammar rule. "Most" is common in everyday speech and some test-takers will pick it. |
| E1-Q02, E2-Q11 | "Neither … nor" agrees with the nearer subject: the formal rule, but plural agreement is widely used in practice. |
| E2-Q05 | "Neither of the proposals **meets**": formal (singular). "Meet" is accepted in informal English. |
| E1-Q14, E2-Q19, E3-Q15 | Inference questions are always somewhat arguable. I reworded E1-Q14 option B as you asked. |

### Logic
| Question | Issue |
|---|---|
| **L2 (all)** | The figure patterns are drawn from rules (rotation, alternating fill, count change, a dot moving between corners), and each wrong option breaks exactly one attribute. The answer is computed, but the *pictures* should be looked at: a distractor could still look confusingly similar at small sizes. |
| L1 (all) | The generator rejects a sequence if a constant-difference or constant-ratio rule would give a different answer. More exotic alternative rules aren't checked. |
| L3-Q05 | Drought : **Famine** (cause-effect). "Desert" is a tempting wrong answer; drought doesn't *cause* a desert in the same direct sense. |
| L3-Q11 | Friction : **Heat** (cause-effect). Friction also opposes motion, but "Motion" isn't offered, to avoid ambiguity. |
| L3-Q15 | Scene : **Play** (part-whole). "Script" was deliberately left out as an option because scenes are also parts of scripts. |
| L4-Q15 | "No auditors are approvers; all approvers are managers → some managers are not auditors." This is valid **only if the groups aren't empty**. The checker assumes every group has at least one member, as these tests usually do. |
| L4 explanations | They're generic ("true in every situation…" / "none follows"). Correct, but less instructive than the hand-written ones. |

### Technical
| Question | Issue |
|---|---|
| T2-Q12 | "93 Annex A controls" is **ISO/IEC 27001:2022**. The 2013 edition had 114 (the explanation says so). |
| T1-Q10, T2-Q02, T3-Q11 | These follow **COSO 2013** (5 components, 17 principles). |
| T2-Q14 | "Report functionally to the board / audit committee." That's standard IIA guidance, but wording differs between the IIA Standards versions. |
| T1-Q14 | Evidence reliability ranking: a general rule with exceptions (e.g. a forged external document). |
| T3-Q17, T3-Q20 | The "best next step" for suspected fraud and for leavers' active accounts can depend on firm policy. The answers follow common practice (escalate, don't act yourself). |
| **All (fixed)** | The correct option used to be the longest in 52 of 60 Technical questions. `tools/rebalance_options.py` rewrote the options (shorter correct answers, longer distractors); now no Technical question has a correct option that is 3+ characters longer than every distractor, and each test uses A/B/C/D exactly 5 times. The only English exception is E3-Q02 ("would have bought" vs "had bought"), where the length difference *is* the grammar being tested. |

## English 4–6: one test per TOEFL ITP question type

Written for this site (original sentences and passages, not taken from TOEFL or prep books), in
`tools/gen_english.py`, which writes `site/data/english-4..6.json`. Fix a question there and rerun it. Each test
has 20 questions, 6 easy, 10 medium and 4 hard (`difficulty` field). A–D are each the answer 5 times, and every
question has an explanation of the rule (or the passage line) plus why the most tempting wrong option fails.

| Test | Content | Timer (`ENGLISH_MINUTES` in `site/js/data.js`) |
|---|---|---|
| E4 Structure | Sentence completion: subject-verb agreement, reduced clauses, inversion, parallelism, conditionals, noun clauses, appositives, comparatives | 13 min (ITP: 40 questions in 25 min ≈ 37.5 s each) |
| E5 Written Expression | Error identification, 4 underlined parts, one wrong: word form, tense, pronouns, prepositions, articles, singular/plural, parallel structure, comparison | 13 min (same pace) |
| E6 Reading | 3 passages (300–314 words: CAM photosynthesis, railway standard time, Ostrom and the commons), 7 + 7 + 6 questions: main idea, detail, inference, vocabulary, reference, author's purpose | 25 min (1 min per question + ~1.5 min to read each passage) |

**Site change.** Error-identification sentences mark their parts as `{A|text}`. `renderQuestionText` in
`site/js/render.js` draws them underlined with the letter beneath (quiz and results review). E1–E3 have no marks,
so they render as before. `check_data.py` checks the typed tests: skill, difficulty mix, A–D spread, marks
matching the options, passage length, 6–7 questions per passage, and the timers in `data.js`.
`tools/rebalance_options.py` now only touches E1–E3 (and Technical), so rerunning it can't reshuffle E4–E6.

**Quality check.**
1. *Blind pass:* a fresh subagent answered all 60 questions without keys (`tools/english_blind_answers.txt`).
   It agreed with all **60/60** keys. Its one "doubt" (E4-Q17) agreed with the key.
2. *Length giveaway, fixed:* in E6 the correct option was the longest in 10 of 20 questions (E6-Q01, Q06, Q07,
   Q09, Q11, Q12, Q14, Q15, Q16, Q20). I shortened those correct options and lengthened a few distractors without
   changing any meaning or answer. Now no correct option in E4 or E6 is more than 2 characters longer than every
   distractor.
3. *Re-check after the fix:* a second fresh subagent, again without keys, judged **every option** of E4 separately
   (trying to rescue each distractor), listed every wrong part in each E5 sentence, and re-answered E6 from the
   passages alone. It found no question with two acceptable answers or none, no second error in any E5 sentence,
   and no reading answer that needs outside knowledge. Its E6 answers matched the keys.

No question needed rewriting because of a disagreement.

### Least sure (E4–E6)
| Question | Issue |
|---|---|
| E4-Q12 | "**Were** the Moon closer…": "Was" is heard in informal inverted conditionals; only "were" is formal. |
| E4-Q17 | "Among the oldest texts **is** the Epic of Gilgamesh": inverted singular subject. "Are" is a common slip, and the blind pass flagged it as a trap, though it agreed with the key. |
| E5-Q19 | "longer than **any** river in Africa" → "any other": a logic-of-comparison rule that many readers pass over. |
| E5-Q04 | "until **they are** eight months old" → "it is": singular "they" is accepted for people, not for an animal. The rule is formal, and some test-takers may not know it. |
| E6-Q04 | Reference "it" = carbon dioxide. "The stored acid" is grammatically nearby; the passage (what becomes sugar) decides it. |

The grammar sentences contain general facts (a blue whale's heart ≈ a small car, the Nile's eleven countries).
These are approximate and don't affect any answer.

## Technical 4–8: one test per topic area, plus a mock exam

Written for this site in `tools/gen_technical.py`, which writes `site/data/technical-4..8.json`. Fix a question there
and rerun it. The schema is the same as T1–T3 (`type` scenario/definition, `level`, 4 options, 20 minutes in
`timeLimitSec`) plus a `topic`, which the results review shows. Each test has 6 easy, 10 medium and 4 hard questions,
uses A–D five times each, and every question has an explanation of why the key is right and why the most tempting
wrong option is wrong. The generator refuses to write a test that repeats a T1–T8 question or breaks these rules.

| Test | Content | Scenario-based |
|---|---|---|
| T4 IT general controls | RBAC, privileged access, SoD, access review (completeness of the user list), movers, provisioning timing, change testing/approval/completeness of the change population, emergency changes, job scheduler access, backups, incidents vs problems, ITGC reliance | 12 / 20 |
| T5 Cybersecurity & frameworks | ISO/IEC 27001:2022 (clauses 4–10, the four Annex A themes, risk treatment, management review), NIST CSF 2.0 functions, phishing, MFA, ransomware, encryption and hashing, patching, SQL injection, broken access control, incident response, scan vs pen test | 9 / 20 |
| T6 Governance, risk & internal control | COSO 2013 components and 17 principles, COBIT 2019 governance vs management and EDM, IIA Three Lines, inherent/residual scoring, risk responses, control types, key controls, material weakness, sampling by frequency, testing automated controls, evidence | 10 / 20 |
| T7 Data, privacy, cloud & third parties | UU PDP (specific data, 3 × 24 h notice, controller/processor, DPIA for automated decisions, sub-processors, rights, 2% fine, cross-border transfer), data owner, analytics follow-up and completeness, shared responsibility (SaaS, IaaS), SOC 1/2 types and CUECs, vendor tiering and scope gaps, RPO, BIA | 12 / 20 |
| T8 Mixed mock exam | All of the above, new questions (ITGC scope, SaaS updates, SoA exclusions, CSF Recover, compensating controls, UU PDP purpose and erasure, SOC 3, DR test vs RTO, fourth parties, JE testing…) | 15 / 20 |

**Site change.** `site/js/data.js` lists Technical tests 1–8 and names them (T1–T3 "Mixed topics"). `check_data.py`
checks T4–T8 for the level mix, A–D spread, scenario share (40%, T8 50%), a type and topic on every question, the
length giveaway below, and repeated question texts across all Technical tests. `tools/rebalance_options.py` now only
touches T1–T3, so it can't reshuffle T4–T8. (Rerunning it isn't idempotent even for T1–T3, so don't rerun it casually.)

**Quality check.**
1. *Facts checked first* (sources below). Questions avoid details likely to change: no OWASP rank numbers (the Top 10
   was revised in 2025), no NIST SP 800-61 phase names (Rev. 3, April 2025, replaced the old four-phase lifecycle with
   the CSF 2.0 functions), and nothing that depends on the UU PDP implementing regulation or the new data protection
   authority.
2. *Length giveaway, fixed before the blind pass:* in the first draft the correct option was the longest in 8–10
   questions per test (up to 11 characters ahead). I lengthened distractors and trimmed keys: now it is the longest in
   2 / 3 / 5 / 3 / 4 questions (T4–T8), and never more than 4 characters longer than every distractor (the one
   exception is T6-Q03, whose options are fixed COSO component names; "Information and communication" is also a
   distractor in T6-Q02).
3. *Absolute-word giveaway, fixed:* 78 distractors but only 2 keys contained words like "always / never / only /
   nothing / at all", so "pick the one without an absolute" would have worked. I rewrote about 50 distractors to remove
   that pattern without changing any answer.
4. *Blind pass:* a fresh subagent answered all 100 questions without keys (`tools/technical_blind_answers.txt`). It
   agreed with **100/100** keys. It listed 8 minor doubts. None was a disagreement, but I tightened four questions:
   - T6-Q14: the key said "go undetected"; it now uses the full definition ("not prevented or detected in time").
   - T7-Q13: the key left out the third route for transfers abroad (consent); now "Equal or higher protection,
     binding safeguards, or consent".
   - T7-Q16: the question asked what the auditor should do in general (reading exceptions, bridge letters…); it now
     asks what to do *about the CUECs*.
   - T8-Q04: the key covered only the missing reason; it now says the exclusion is unjustified and doesn't fit the risks.
5. *Re-check:* a second fresh subagent answered the four changed questions blind and matched all four keys, with no
   other option it found defensible.

No question needed rewriting because of a disagreement.

**Browser test.** A full exam run of T4 (timer 20:00; the review shows topic, key and explanation for all 20; the
3 wrong answers went to the wrong-answer bank), and T8 once (submitted with one question unanswered and one wrong,
scored 18/20, review correct). At 375 px width the section page, the quiz and the results review have no horizontal
overflow. The test attempts were removed from the browser's progress afterwards.

### Sources used for T4–T8
- ISO/IEC 27001:2022 Annex A, 93 controls in 4 themes (37 / 8 / 14 / 34):
  [Secureframe](https://secureframe.com/hub/iso-27001/controls), [ISMS.online](https://www.isms.online/iso-27001/annex-a-2022/),
  [GAICC](https://gaicc.org/blog/iso-27001-annex-a-controls-list/)
- NIST CSF 2.0, six functions with Govern new: [NIST CSWP 29](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf)
- NIST SP 800-61 Rev. 3 (April 2025): [NIST news](https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations),
  [CSRC](https://csrc.nist.gov/projects/incident-response)
- UU PDP (Law 27/2022): official text [JDIH BPK](https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022),
  [pasal.id](https://pasal.id/peraturan/uu/uu-no-27-tahun-2022), bilingual text
  [ABNR](https://www.abnrlaw.com/lib/files/IND-ENG-UU%2027-2022%20Pelindungan%20Data%20Pribadi%20(ABNR).pdf).
  Articles used: 4 (specific vs general data), 9 (withdraw consent), 16 and 20 (principles and bases), 34 (impact
  assessment incl. automated decisions), 43–45 (erasure/destruction and notifying the subject), 46 (3 × 24 h notice),
  51 (processor on instructions; written approval before another processor), 53 (DPO), 56 (transfers abroad),
  57 (fine up to 2% of annual revenue), 74 (2-year transition, ended 17 Oct 2024).
- SOC 1 / SOC 2 / Type 1 vs 2, trust services criteria: [AICPA SOC 2 description criteria](https://www.aicpa-cima.com/resources/download/get-description-criteria-for-your-organizations-soc-2-r-report),
  [Linford & Co](https://linfordco.com/blog/soc-1-vs-soc-2-audit-reports/), [System and organization controls (Wikipedia)](https://en.wikipedia.org/wiki/System_and_organization_controls)
- IIA Three Lines Model (2020): [IIA position paper](https://www.theiia.org/globalassets/documents/resources/the-iias-three-lines-model-an-update-of-the-three-lines-of-defense-july-2020/three-lines-model-updated-english.pdf)
- COBIT 2019, 40 objectives, EDM governance domain: [ISACA](https://www.isaca.org/resources/news-and-trends/industry-news/2019/employing-cobit-2019-for-enterprise-governance-strategy)
- OWASP Top 10:2025 (broken access control still includes IDOR): [OWASP](https://owasp.org/Top10/2025/)
- Cloud shared responsibility: [Microsoft Learn](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility)
- COSO 2013 (5 components, 17 principles) and the PCAOB AS 2201 material-weakness definition are well established and
  already used by T1–T3; they weren't looked up again.

### Least sure (T4–T8)
| Question | Issue |
|---|---|
| T7-Q07 | Fine "up to 2% of annual revenue": Article 57(3) says 2% of annual income or revenue *for the violation variable*. How that variable is calculated awaits the implementing regulation, so the question asks only for the cap. |
| T7-Q13 | Transfers abroad: the key summarises Article 56's three routes. The details (who judges "equal or higher" protection) are left to implementing rules and the new authority. Sector rules (e.g. financial services) may add localisation requirements the question doesn't cover. |
| T6-Q17 | "Test of one" for an automated control with effective ITGCs is common Big 4 practice, not a rule in a standard. Some methodologies test a few items. |
| T8-Q12 | Erasure on request assumes none of the exceptions apply (the question says so). The duty to tell the subject comes from Article 45. |
| T4-Q10 | "40% emergency changes most likely indicates bypassing": an inference. The key is the only option that fits, but a real audit would investigate first. |

---

# Verification pass vs Verified PDF

Source: `PwC_Aptitude_Test_Verified.pdf` (89 pages, text only, no images; created 2026-09-27 17:39 with LibreOffice).
**No JSON was changed in this pass.** This section is a report only.

## What the Verified PDF is

- **Coverage:** Numerical Tests 1–5 (100 questions) and Verbal Tests 1–7 (104 questions), so **204 of the site's 414
  questions**. It does **not** cover N6/V8 (the entrance-test paper) or the generated English/Logic/Technical sections.
- **Numbering:** It matches the original PDF and the site ids one-to-one (N1-Q01 … V7-Q15, including the missing V4-Q04).
  I checked this by matching every question's text against the site JSON: all 204 matched and none were missing or extra.
- **Content:** It has the full question, the options, the chart data as a table (said to be "checked against the page image"),
  **a verified answer and a worked solution for every question**, and a correction note where it disagrees with the original key.
  Page 2 lists all its corrections, with a status for each: CORRECT / WRONG ANSWER / WRONG EXPLANATION / AMBIGUOUS / SOURCE ISSUE.
- **It is not independent of this site.** Many of its solutions repeat the site's explanations almost word for word (e.g.
  V2-Q06 "the wider push aims at information and protection… doesn't say what the documentation alone is for", V5-Q12
  "more variety does not necessarily mean more courses", N3-Q04's "$60,000 if departments spend equally", N1-Q19's "29%, closest to D").
  So when it **agrees** with the site, that is weak confirmation. When it **disagrees**, it is disagreeing with the
  original PDF key (V2-Q11, V4-Q05) or re-arguing a known ambiguity (N2-Q07). It never brings in new data.

## Method

1. I built a copy of all 204 questions **with `answer`, `verifiedAnswer`, `explanation` and `flag` removed** and answered them from that
   copy: numerical by recomputing from the chart/table data in `site/data`, verbal from the passage only. I saved those answers
   to a file before opening any of the Verified PDF's answer lines. *Caveat:* before that step I had already read this REVIEW.md
   (which holds my earlier judgments) and the Verified PDF's one-page "Corrections at a Glance" while working out its structure, so the
   pass is blind to the per-question keys but not fully blind to the earlier review.
2. I then parsed all 204 "Verified Answer" lines and compared the four columns.
3. No numerical value looked doubtful. My recomputations matched the site's chart data in every case, so I didn't need to go back to the chart images.

## Result by class

| Class | Count | Questions |
|---|---|---|
| All four agree | **172** | (includes 6 already-flagged questions where everyone agrees: N2-Q11, N3-Q01 disputed; V2-Q10, V3-Q07, V4-Q09, V4-Q15 truncated) |
| Site already corrected, Verified PDF and I both confirm | **14** | N1-Q01, N1-Q02, N1-Q07, N1-Q19 (dropped), N2-Q02, N2-Q17, N3-Q04, N3-Q08, V1-Q13, V2-Q03, V3-Q01, V3-Q09, V4-Q06, V7-Q06 |
| **Likely real fix** (Verified differs from the PDF key and the site still uses the PDF key) | **0** | none |
| **Needs a decision** (Verified differs from a recomputed/disputed site answer) | **3** | N2-Q07, V2-Q11, V4-Q05 |
| **Suspect** (Verified differs from my blind answer) | **15** | N1-Q10, N1-Q13, V1-Q02, V1-Q14, V2-Q02, V2-Q06, V2-Q13, V2-Q15, V3-Q10, V3-Q12, V3-Q13, V4-Q10, V5-Q12, V6-Q14, V7-Q14 |

**The Verified PDF finds no wrong answer that the site doesn't already handle.** All 11 of its "WRONG ANSWER" items (N1-Q01, Q02; N2-Q02,
Q17; N3-Q04, Q08; V1-Q13; V2-Q03; V3-Q09; V4-Q05; V4-Q06) are already corrected on the site. Ten of them match the site's answer. The
eleventh, V4-Q05, is corrected to a *different* answer (see below).

## Needs a decision

In all three, my blind answer sides with **the site**, not the Verified PDF.

### N2-Q07: site **B (31.31%, PDF key, disputed)**, Verified **A (29.7%)**, mine: 29.2%, no exact option
- *Verified PDF:* 2009 total = 4.0m × 1.08 = 4.32m; exploration = 1.16m + 0.1m = 1.26m → **29.17%**, "closest to A (29.7%), probably a misprint".
  It says the key double-counts: exploration grows 8% *and* gets +£100k while the total only grows 8%, so the other divisions must shrink.
- *PDF key / site:* (0.29 × 4.32m + 0.1m) ÷ 4.32m = **31.31%**, reading "an additional £100,000" as on top of exploration's normal share.
  That is an exact option match, and nothing stops the other divisions from shrinking a little.
- *Mine (blind):* both readings are possible. The more literal one gives 29.2%, which **isn't an option** (A is 29.7%).
- **My recommendation: keep B, disputed (no change).** Under our numerical rules, "recomputed" needs my answer to *match* an option,
  and 29.2 ≠ 29.7. If you don't want to score an ambiguous question, the other option is to **drop** it (like N1-Q19), not to switch it to A.

### V2-Q11: site **True (recomputed, your earlier decision)**, Verified **Cannot say (= PDF key)**, mine **True**
- *Verified PDF:* "The study used employees' own ratings of their bosses, so a link with actual incompetence cannot be confirmed."
- *Site / mine:* the statement is about employees "that have incompetent bosses". The passage says those who *categorised* their boss as
  incompetent were 25% more at risk of serious heart disease, with external factors controlled. That is a stated link.
- The Verified PDF's argument is the same "rated, not shown" point already recorded above as "the only argument for Cannot say".
  It adds nothing new.
- **My recommendation: keep True.** If you'd rather defer to the key, set it back to Cannot say and flag it **disputed**, with this
  note as the alternative reading.

### V4-Q05: site **False (recomputed, confirmed)**, Verified **Cannot say**, PDF key **True**, mine **False**
- *Verified PDF:* 40% is a *future* projection ("is set to rise to 40%"), and today's share isn't given, so Cannot say. But its own step 3
  says "even using the projection, 40% aged 65+ means 60% under 65, not less than 60%".
- *Site / mine:* "set to **rise to** 40%" means today's share is below 40%, so more than 60% are under 65 now. Even at 40%, exactly 60%
  would be under 65, not less. Every reading contradicts "less than 60%", so the statement is **False**.
- **My recommendation: keep False.** The Verified PDF's own reasoning contradicts its Cannot say: it only works if "rise to" says
  nothing about the current level.

## Suspect: the Verified PDF differs from my blind answer

Two of these were my mistakes, and I withdraw them after rechecking. For the others, the Verified PDF agrees with the site, so nothing
changes unless you want it to. None of them is strong enough on its own to change a scored answer.

| Question | Site / Verified | Mine (blind) | Assessment |
|---|---|---|---|
| **N1-Q10** | E / E | C | **My error.** Insurance 195/2,704 = 7.2% is also ≈ 7%, as well as Utilities (7.0%). E is right. |
| **N1-Q13** | B / B | C | **Both are right.** 297:380 = 1:1.28 (B) = 0.78:1 (C). The Verified PDF says so too. The site scores only B, **with no flag**: a user who picks C is marked wrong for a correct answer. **Suggest:** add a `disputed` flag saying B and C are the same ratio (or accept both, if the quiz engine can). |
| V1-Q02 | CS / CS | F (low) | "Sluggish growth" is still growth, which contradicts a "depression". But "depressed market" can loosely mean a weak one. Verified's reasoning is fair. Keep CS. |
| V1-Q14 | F / F | CS (low) | "Many… are often inaccurate" doesn't strictly give "most". But "typically they tend to be over-optimistic" supports F. Keep F. |
| V2-Q02 | F (disputed) / F | CS | Verified: "the law does distinguish by hazard". The passage only says immediate threats must be cleaned up; it never says long-term ones needn't be, and the statement is about *litigation*. This is the existing dispute and the Verified PDF adds nothing new. Keep as is. |
| **V2-Q06** | CS / CS | F | **My error.** The *push* aims at information and protection, but the protection part is the cooling-off period. The documentation alone could well be only for information. CS is right. |
| V2-Q13 | T (disputed) / T | CS (low) | Existing dispute; Verified repeats the key's view ("wanting funding implies wanting work"). Keep as is. |
| V2-Q15 | F (disputed) / F | CS (low) | Verified's reasoning is **weak**: "Italy and Britain must increase *their share*, so other countries also fund it". Having a share doesn't prove there are other contributors. See also the explanation issue below. Keep F disputed. |
| V3-Q10 | F / F | CS (low) | The passage sets early detection (P-waves) against prediction, so "could be used to predict" is contradicted in its terms. F is defensible. Keep. |
| V3-Q12 | T (truncated) / T | CS (visible text) | Already flagged truncated. Verified admits it "cannot be fully verified". Keep. |
| V3-Q13 | F / F | CS (low) | The experiments were run "under scientifically controlled conditions"; the criticism is about realism, not validity. F is defensible. Keep. |
| V4-Q10 | CS / CS | F (medium) | Stress has other causes (conditions, hours, colleagues), so family time can't guarantee no stress, which leans False. But the passage doesn't address it directly. Keep CS. |
| V5-Q12 | CS / CS | T (medium) | Verified: "variety ≠ number". Strict but valid. Keep CS. |
| V6-Q14 | T (disputed) / T | CS | Existing dispute. Verified: "managers are staff and users, so they have passwords". It still doesn't show that *all* managers have *their own*. Keep as is. |
| V7-Q14 | F (disputed) / F | CS | Existing dispute. Verified asserts "other causes would still have increased the damage", which the passage doesn't quantify. Keep as is. |

## Not covered by the Verified PDF but had problems before

- **N6/V8 (entrance test):** V8-Q06 (recomputed to Cannot say), V8-Q12 and V8-Q14 (disputed, ambiguous relation), N6-Q06 (42, recomputed + disputed),
  N6-Q15 (464,800, recomputed + disputed), V8-Q04 (corrected word pair) and V8-Q02 (two grammatical readings). These can only be checked against
  `pdf-pwc-entrance-test-amp-answer_compress.pdf` and `tools/verify_entrance.py`.
- **English / Logic / Technical (180 generated questions):** no external source at all. The "least sure" list above still applies.

## Stale explanations

I checked all 204 covered explanations against the answer the site scores. The numerical ones were checked by script (does the scored
option's value appear in the working) and then read one by one. I read all 104 verbal ones.

- **No explanation contradicts its scored answer.** Every recomputed question shows the corrected working, and every disputed one explains the key it keeps.
- The Verified PDF lists "WRONG EXPLANATION" items that are not in the notes above: N3-Q19 (Level 2/3 labels swapped), N4-Q16 (used 36 enquiries), and
  N5-Q15 (units). **The site's explanations for all three are already correct.** So are N4-Q20 and the other items listed earlier.
- **One wording issue, V2-Q15:** the explanation says "the extra cost falls on all the participating countries… **not just Italy and Britain**",
  but the flag note on the same question says "the passage doesn't say whether other countries participate". The two contradict each other.
  The answer (False) is unaffected. **Fixed** (see Decisions below).
- **N1-Q19** (dropped) shows the PDF's working ending in "'24%'". That's intentional, because the question isn't scored and the flag note explains the slip.

## Decisions (applied)

Every other answer stays as it was. No scored answer changed. N1-Q13 now also accepts C.

| Question | Scored | Change |
|---|---|---|
| N2-Q07 | B (unchanged) | Flag stays **disputed**. The note now gives both readings: the key's (29% share of the 8%-larger total + £100,000 → 31.31%, B) and the plain one ((1.16m + 0.1m) ÷ 4.32m = 29.2%, which matches no option; A is 29.7%). |
| V2-Q11 | True (unchanged) | Flag changed from recomputed to **disputed**. The note says the original key and another source say Cannot say, because the passage speaks of employees who *categorised* their boss as incompetent (a perception), not bosses shown to be incompetent. `answerSource` stays `recomputed`, so the quiz still shows "Source PDF key: C · This site uses: A". |
| V4-Q05 | False (unchanged) | Flag changed from recomputed to **disputed**. The note says the original key was True and another source says Cannot say, then explains why False is used: "set to rise to 40%" implies the current 65+ share is below 40%, so more than 60% are under 65 now, and even the projected 40% gives exactly 60%, not less. `answerSource` stays `recomputed`. |
| N1-Q13 | B **or C** | New optional field `acceptedAnswers: ["B", "C"]` plus a **disputed** flag explaining that 1:1.28 and 0.78:1 are the same ratio. The explanation shows both divisions. |
| V2-Q15 | False (unchanged) | The explanation no longer says "not just Italy and Britain". It now says Italy and Britain must increase their share, and that the passage doesn't say they cover the cost alone. |

**Engine change for `acceptedAnswers` (small):** `data.js` gains `acceptedAnswers(q)` (the list, or just the scored answer) and
`isAccepted(q, letter)`. The attempt score (`quiz.js`), the practice navigator colours (`quiz-view.js`), the option highlighting and the
verdict (`render.js`) all use it. Every accepted option is highlighted green, and the verdict reads "Correct answers: B (1:1.28) or C (0.78:1)".
`correctAnswer(q)` is unchanged, so saved attempts and the wrong-answer bank keep working. `tools/check_data.py` checks that
`acceptedAnswers` lists 2+ distinct options, includes the scored answer and comes with a flag note.

## Full comparison (all 204 covered questions)

Verbal: T = True, F = False, CS = Cannot say. "Site scores" is `verifiedAnswer` if set, otherwise the PDF key, plus the flag type,
**as it was during the pass, before the decisions above** (since then, N1-Q13 accepts B or C and is flagged disputed, and the flags for V2-Q11 and V4-Q05 are now disputed).

**Numerical 1**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| N1-Q01 | B | D (recomputed) | D | D | fix confirmed |
| N1-Q02 | B | D (recomputed) | D | D | fix confirmed |
| N1-Q03 | B | B | B | B | ok |
| N1-Q04 | C | C | C | C | ok |
| N1-Q05 | B | B | B | B | ok |
| N1-Q06 | C | C | C | C | ok |
| N1-Q07 | C | E (recomputed) | E | E | fix confirmed |
| N1-Q08 | A | A | A | A | ok |
| N1-Q09 | E | E | E | E | ok |
| N1-Q10 | E | E | E | C → **E** on recheck | **suspect** |
| N1-Q11 | E | E | E | E | ok |
| N1-Q12 | E | E | E | E | ok |
| N1-Q13 | B | B | B | C (= B) | **suspect** |
| N1-Q14 | B | B | B | B | ok |
| N1-Q15 | A | A | A | A | ok |
| N1-Q16 | C | C | C | C | ok |
| N1-Q17 | A | A | A | A | ok |
| N1-Q18 | C | C | C | C | ok |
| N1-Q19 | B | — (not scored) (dropped) | no option | none (dropped) | fix confirmed |
| N1-Q20 | C | C | C | C | ok |

**Numerical 2**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| N2-Q01 | E | E | E | E (264) | ok |
| N2-Q02 | E | D (recomputed) | D | D | fix confirmed |
| N2-Q03 | D | D | D | D | ok |
| N2-Q04 | C | C | C | C | ok |
| N2-Q05 | A | A | A | A | ok |
| N2-Q06 | C | C | C | C | ok |
| N2-Q07 | B | B (disputed) | A | 29.2% → nearest A | **needs decision** |
| N2-Q08 | C | C | C | C | ok |
| N2-Q09 | A | A | A | A | ok |
| N2-Q10 | A | A | A | A | ok |
| N2-Q11 | B | B (disputed) | B | B (58,000 typo) | ok |
| N2-Q12 | E | E | E | E | ok |
| N2-Q13 | D | D | D | D | ok |
| N2-Q14 | C | C | C | C | ok |
| N2-Q15 | B | B | B | B | ok |
| N2-Q16 | B | B | B | B | ok |
| N2-Q17 | B | A (recomputed) | A | A | fix confirmed |
| N2-Q18 | B | B | B | B | ok |
| N2-Q19 | C | C | C | C | ok |
| N2-Q20 | C | C | C | C | ok |

**Numerical 3**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| N3-Q01 | C | C (disputed) | C | C | ok |
| N3-Q02 | B | B | B | B | ok |
| N3-Q03 | C | C | C | C | ok |
| N3-Q04 | B | E (disputed) | E | E | fix confirmed |
| N3-Q05 | E | E | E | E | ok |
| N3-Q06 | A | A | A | A | ok |
| N3-Q07 | D | D | D | D | ok |
| N3-Q08 | D | E (recomputed) | E | E | fix confirmed |
| N3-Q09 | E | E | E | E | ok |
| N3-Q10 | E | E | E | E | ok |
| N3-Q11 | C | C | C | C | ok |
| N3-Q12 | E | E | E | E | ok |
| N3-Q13 | D | D | D | D | ok |
| N3-Q14 | E | E | E | E | ok |
| N3-Q15 | D | D | D | D | ok |
| N3-Q16 | C | C | C | C | ok |
| N3-Q17 | A | A | A | A | ok |
| N3-Q18 | D | D | D | D | ok |
| N3-Q19 | D | D | D | D | ok |
| N3-Q20 | D | D | D | D | ok |

**Numerical 4**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| N4-Q01 | D | D | D | D | ok |
| N4-Q02 | A | A | A | A | ok |
| N4-Q03 | A | A | A | A | ok |
| N4-Q04 | E | E | E | E | ok |
| N4-Q05 | C | C | C | C | ok |
| N4-Q06 | A | A | A | A | ok |
| N4-Q07 | E | E | E | E | ok |
| N4-Q08 | B | B | B | B | ok |
| N4-Q09 | C | C | C | C | ok |
| N4-Q10 | A | A | A | A | ok |
| N4-Q11 | E | E | E | E | ok |
| N4-Q12 | C | C | C | C | ok |
| N4-Q13 | A | A | A | A | ok |
| N4-Q14 | C | C | C | C | ok |
| N4-Q15 | A | A | A | A | ok |
| N4-Q16 | C | C | C | C | ok |
| N4-Q17 | E | E | E | E | ok |
| N4-Q18 | C | C | C | C | ok |
| N4-Q19 | A | A | A | A | ok |
| N4-Q20 | C | C | C | C | ok |

**Numerical 5**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| N5-Q01 | A | A | A | A | ok |
| N5-Q02 | A | A | A | A | ok |
| N5-Q03 | D | D | D | D | ok |
| N5-Q04 | B | B | B | B | ok |
| N5-Q05 | C | C | C | C | ok |
| N5-Q06 | C | C | C | C | ok |
| N5-Q07 | B | B | B | B | ok |
| N5-Q08 | B | B | B | B | ok |
| N5-Q09 | E | E | E | E | ok |
| N5-Q10 | A | A | A | A | ok |
| N5-Q11 | E | E | E | E | ok |
| N5-Q12 | C | C | C | C | ok |
| N5-Q13 | D | D | D | D | ok |
| N5-Q14 | A | A | A | A | ok |
| N5-Q15 | D | D | D | D | ok |
| N5-Q16 | E | E | E | E | ok |
| N5-Q17 | D | D | D | D | ok |
| N5-Q18 | E | E | E | E | ok |
| N5-Q19 | D | D | D | D | ok |
| N5-Q20 | B | B | B | B | ok |

**Verbal 1**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| V1-Q01 | CS | CS | CS | CS | ok |
| V1-Q02 | CS | CS | CS | F | **suspect** |
| V1-Q03 | T | T | T | T | ok |
| V1-Q04 | CS | CS | CS | CS | ok |
| V1-Q05 | CS | CS | CS | CS | ok |
| V1-Q06 | CS | CS | CS | CS | ok |
| V1-Q07 | F | F | F | F | ok |
| V1-Q08 | CS | CS | CS | CS | ok |
| V1-Q09 | F | F | F | F | ok |
| V1-Q10 | T | T | T | T | ok |
| V1-Q11 | F | F | F | F | ok |
| V1-Q12 | CS | CS | CS | CS | ok |
| V1-Q13 | T | CS (recomputed) | CS | CS | fix confirmed |
| V1-Q14 | F | F | F | CS | **suspect** |
| V1-Q15 | T | T | T | T | ok |

**Verbal 2**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| V2-Q01 | T | T | T | T | ok |
| V2-Q02 | F | F (disputed) | F | CS | **suspect** |
| V2-Q03 | T | CS (recomputed) | CS | CS | fix confirmed |
| V2-Q04 | CS | CS | CS | CS | ok |
| V2-Q05 | CS | CS | CS | CS | ok |
| V2-Q06 | CS | CS | CS | F | **suspect** |
| V2-Q07 | F | F | F | F | ok |
| V2-Q08 | T | T | T | T | ok |
| V2-Q09 | CS | CS | CS | CS | ok |
| V2-Q10 | CS | CS (truncated) | CS | CS | ok |
| V2-Q11 | CS | T (recomputed) | CS | T | **needs decision** |
| V2-Q12 | T | T | T | T | ok |
| V2-Q13 | T | T (disputed) | T | CS | **suspect** |
| V2-Q14 | CS | CS | CS | CS | ok |
| V2-Q15 | F | F (disputed) | F | CS | **suspect** |

**Verbal 3**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| V3-Q01 | — (none) | CS (missing-key) | CS | CS | fix confirmed |
| V3-Q02 | T | T | T | T | ok |
| V3-Q03 | F | F | F | F | ok |
| V3-Q04 | T | T | T | T | ok |
| V3-Q05 | CS | CS | CS | CS | ok |
| V3-Q06 | CS | CS | CS | CS | ok |
| V3-Q07 | CS | CS (truncated) | CS | CS | ok |
| V3-Q08 | F | F | F | F | ok |
| V3-Q09 | T | CS (recomputed) | CS | CS | fix confirmed |
| V3-Q10 | F | F | F | CS | **suspect** |
| V3-Q11 | CS | CS | CS | CS | ok |
| V3-Q12 | T | T (truncated) | T | CS (visible text) | **suspect** |
| V3-Q13 | F | F | F | CS | **suspect** |
| V3-Q14 | T | T | T | T | ok |
| V3-Q15 | CS | CS | CS | CS | ok |

**Verbal 4**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| V4-Q01 | F | F | F | F | ok |
| V4-Q02 | CS | CS | CS | CS | ok |
| V4-Q03 | F | F | F | F | ok |
| V4-Q05 | T | F (recomputed) | CS | F | **needs decision** |
| V4-Q06 | F | T (recomputed) | T | T | fix confirmed |
| V4-Q07 | CS | CS | CS | CS | ok |
| V4-Q08 | T | T | T | T | ok |
| V4-Q09 | CS | CS (truncated) | CS | CS | ok |
| V4-Q10 | CS | CS | CS | F | **suspect** |
| V4-Q11 | F | F | F | F | ok |
| V4-Q12 | CS | CS | CS | CS | ok |
| V4-Q13 | T | T | T | T | ok |
| V4-Q14 | T | T | T | T | ok |
| V4-Q15 | CS | CS (truncated) | CS | CS | ok |

**Verbal 5**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| V5-Q01 | CS | CS | CS | CS | ok |
| V5-Q02 | CS | CS | CS | CS | ok |
| V5-Q03 | T | T | T | T | ok |
| V5-Q04 | T | T | T | T | ok |
| V5-Q05 | CS | CS | CS | CS | ok |
| V5-Q06 | T | T | T | T | ok |
| V5-Q07 | T | T | T | T | ok |
| V5-Q08 | T | T | T | T | ok |
| V5-Q09 | F | F | F | F | ok |
| V5-Q10 | CS | CS | CS | CS | ok |
| V5-Q11 | F | F | F | F | ok |
| V5-Q12 | CS | CS | CS | T | **suspect** |
| V5-Q13 | F | F | F | F | ok |
| V5-Q14 | CS | CS | CS | CS | ok |
| V5-Q15 | T | T | T | T | ok |

**Verbal 6**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| V6-Q01 | F | F | F | F | ok |
| V6-Q02 | CS | CS | CS | CS | ok |
| V6-Q03 | F | F | F | F | ok |
| V6-Q04 | T | T | T | T | ok |
| V6-Q05 | T | T | T | T | ok |
| V6-Q06 | F | F | F | F | ok |
| V6-Q07 | CS | CS | CS | CS | ok |
| V6-Q08 | T | T | T | T | ok |
| V6-Q09 | T | T | T | T | ok |
| V6-Q10 | F | F | F | F | ok |
| V6-Q11 | CS | CS | CS | CS | ok |
| V6-Q12 | F | F | F | F | ok |
| V6-Q13 | CS | CS | CS | CS | ok |
| V6-Q14 | T | T (disputed) | T | CS | **suspect** |
| V6-Q15 | F | F | F | F | ok |

**Verbal 7**

| Question | PDF key | Site scores | Verified PDF | Mine (blind) | Class |
|---|---|---|---|---|---|
| V7-Q01 | F | F | F | F | ok |
| V7-Q02 | CS | CS | CS | CS | ok |
| V7-Q03 | T | T | T | T | ok |
| V7-Q04 | CS | CS | CS | CS | ok |
| V7-Q05 | F | F | F | F | ok |
| V7-Q06 | CS | T (recomputed) | T | T | fix confirmed |
| V7-Q07 | T | T | T | T | ok |
| V7-Q08 | T | T | T | T | ok |
| V7-Q09 | CS | CS | CS | CS | ok |
| V7-Q10 | F | F | F | F | ok |
| V7-Q11 | T | T | T | T | ok |
| V7-Q12 | CS | CS | CS | CS | ok |
| V7-Q13 | T | T | T | T | ok |
| V7-Q14 | F | F (disputed) | F | CS | **suspect** |
| V7-Q15 | CS | CS | CS | CS | ok |

## Logic Subtest 5: imported figural patterns (extra hard)

17 picture questions imported from `figural-test-extra-hard-part-1/` (not committed; the images are copied to
`site/img/figural-hard-01.png` … `-17.png`). Built by `python tools/import_figural.py`, which also writes
`site/data/logic-5.json`, including the Q9 decision (its `OVERRIDES` table), so re-running it keeps Q9 scored D. Every question has `"source": "imported"` and shows an "Imported, key from source" label.
The **scored answer is the source key** (`jawaban.txt`) except for **Q9**, which scores D by the owner's decision
(see below). Disagreements are flagged `disputed`.
Timer: 17 minutes, set in one place, `SECTIONS.logic.testMinutes[5]` in `site/js/data.js` (the JSON has no `timeLimitSec`).

**Format of the source**
- Q1–Q11: top row = 5-figure series, bottom row = options (A)–(E), lettered in the image.
- Q12–Q14: 4-figure series, "Apa yang berikutnya?", **6 options with no letters printed**. The key uses A–F, read
  left to right; in Q14 the options wrap, so F is the one on the second row. The question text says this.
- Q15–Q17: analogies (A : B = C : ?; in Q17 the ? is the second figure), options A–E printed in pink.
- `jawaban.txt` covers all 17. Its note "Soal pilihan A-F" appears after Q11 but only Q12–Q14 have six options;
  Q15–Q17 have five (their keys C, C, A are all within A–E).
- **Q3 and Q4 are the same puzzle** (Q4 is a lower-resolution capture with a "subscribe" badge). Both are kept, as
  asked (17 questions), and both keys say C.

**Blind check.** I solved every question from the images and wrote my answers with a confidence level to
`tools/figural_blind_answers.txt` before comparing. Caveat: I had already read `jawaban.txt` once in step 1 (format
check), so this was not perfectly blind; the low-confidence answers below in particular may have been pulled toward
the key. Result: **16 of 17 agree; 1 disagreement (Q11)**.

| Q | Key | Mine | Confidence | Rule I see |
|---|---|---|---|---|
| 1 | A | A | high | Arrow turns 90° and 45° anticlockwise in turn (S, E, NE, NW, W → S); hook on the bar flips down/up → up |
| 2 | B | B | medium | End symbols reorder by "first to the end" and "swap pairs" in turn, comb flips side; frame 5 = frame 1 → frame 6 = frame 2 |
| 3 | C | C | **low** | Big symbol = previous frame's small symbol flipped top-to-bottom (S→Ƨ, N→И, L→Γ, ⅄→Y), so the big zigzag fits C and D. The small symbol decides between them and I found no rule for it; I chose C only because S already appeared in frame 1 |
| 4 | C | C | **low** | Same puzzle as Q3 |
| 5 | E | E | high | n-sided polygon cut into n regions, n = 3…7 → octagon with 8 regions |
| 6 | D | D | high | Circle, triangle, square; each new shape appears small inside the previous one first → square holding a pentagon |
| 7 | B | B | medium | Right side loses lines from the top on even frames: 1, then 3 → 5; left side full |
| 8 | A | A | medium | Arrow jumps 2 of the 6 sectors clockwise, direction cycling SE, SW, NW; dot moves 1 sector clockwise |
| 9 | C | C | **low** | Six arcs; no rule found that singles out one option (frame 3 is frame 2 reversed and frame 4 is frame 1 reversed, but that does not give a unique frame 6). **Now scored D**, see below |
| 10 | E | E | medium | One symbol moves per step, 2, 3, 4, 2 cells anticlockwise round the border; next the X moves 3 → bottom-middle |
| **11** | **B** | **A** | high | **Disputed.** See below |
| 12 | B | B | high | Two squares on a diagonal alternate with four squares; the diagonal switches → top-left + bottom-right |
| 13 | D | D | **low** | Each frame = previous frame turned 90° clockwise + one new line (checked for frames 2–4). That leaves option 2 (B) and option 4 (D), which differ only in which diagonal is added; I found no rule for the new line's position, so D is no better than B on my reasoning |
| 14 | F | F | high | Dots 2→6, arrows 1→5; the fan of arrows starts 45° further clockwise each step → S, SW, W, NW, N |
| 15 | C | C | medium | Big shape gains a side; the two small shapes swap inside/outside; outside shape at top right |
| 16 | C | C | medium | Big shape joined with its shaded mirror image; rectangles → triangles, middle shaded |
| 17 | A | A | medium | Small shapes above/below swap; the shape inside the block loses a side (C's pentagon → D's diamond, so A's hexagon → pentagon). At first I misread C's pentagon as a hexagon and picked C; the zoomed image shows a pentagon |

**Q11 (disputed, key kept: B).** Three parts: a top bar with a slanted hook, a middle bar with a slanted hook, and a
bottom bracket. Frame 5 is the same drawing as frame 1 (measured: 0.4% of pixels differ, vs 5.6% between
frames 1 and 2). Going 1→2 the middle bar turns 180°
(hook at the right going down → hook at the left going up); 2→3 the top bar and the bracket both turn 180°; 3→4 the
middle bar turns back; 4→5 top and bracket turn back. So the steps alternate "middle" and "top + bottom", and
frame 6 = frame 5 with the middle bar turned = frame 2 = **option A** (by eye the same drawing; measured, A is the
closest option to frame 2: 3.7% of pixels differ, against 5.6–8.3% for B–E). The key's **B** has
the middle bar's hook at the right bending *up*, a shape that appears in no frame. I can't find a rule that gives B.
Confidence that A is right: fairly high, but these puzzles are easy to misread. The site scores B and shows my
reasoning as a note after you answer.

**Explanations.** One-line explanations are filled in where I'm confident (Q1, 2, 5, 6, 7, 8, 10, 12, 14, 15, 16, 17).
They are **empty for Q3, Q4, Q13** (rule not clear to me), **Q9** (see below) and **Q11** (disputed; the flag note
explains instead).

**Q9 (decision: score D).** Source key C; the blind check also gave C, but only as a low-confidence pick with no rule.
The owner decided the answer is **D** (the option with three closed ovals). The question keeps `answer: "C"` (source
key), gets `verifiedAnswer: "D"` (scored) and flag `disputed` with a neutral note. **The rule for D was not supplied**
(the decision left the rule as a placeholder), so the explanation is empty and the note doesn't state a rule. Add the
rule to the explanation and the note once it's written down: both live in `tools/import_figural.py` (`QUESTIONS[9]`
and `OVERRIDES[9]`), then re-run the script.

### Least sure (figural)
1. **Q9**: scored D by decision (source key C); no written rule yet for either answer.
2. **Q13**: B and D both fit the rotate-and-add rule; the key's D is plausible, not proven.
3. **Q3 / Q4**: the big symbol is certain (C or D); the small letter that decides between them is not.
4. **Q11**: the one disagreement; recheck by comparing option A with frame 2.
5. **Q7**: counting lines in small teeth. The 1, 3, 5 progression is my reading of a low-resolution image.

## Logic Subtests 6–9: imported figural question bank

68 picture questions from `[4]Bank_Soal_Psikotes_Figural_Spasial.pdf` (not committed; neither are any full-page
renders). Built by `python tools/import_figural_bank.py`, which reads the PDF (it is never modified), takes each
question's embedded image and re-lays its cells on a grid (stimulus rows, a line, then options A–D) so it stays
readable at phone width, and writes `site/img/figbank-NNN.png` and `site/data/logic-6.json` … `logic-9.json`. All
review decisions live in the script's tables (`AMBIGUOUS`, `DISPUTED`, `EXPLANATIONS`), so re-running it keeps them.
Every question has `"source": "imported"`, the "Imported, key from source" label, and a small "Bank no. N" label
(`sourceRef`) with its number in the PDF. Timer: 17 minutes for each subtest, one value (`FIGURAL_BANK_MINUTES` in
`site/js/data.js`).

| Subtest | Topic in the PDF | Bank numbers (sedang + sulit only) | Scored |
|---|---|---|---|
| L6 Figural analogies | Analogi Figural (1–25) | 5, 7, 9–22, 24 | 15 of 17 |
| L7 Odd one out | Klasifikasi & Pengelompokan Bentuk (26–50) | 28, 29, 31, 33–35, 37, 39–45, 47, 49, 50 | 16 of 17 |
| L8 Figural series | Seri/Pola Figural (51–75) | 51–57, 59–62, 64, 68, 70–73 | **5 of 17** |
| L9 Figural matrices | Matriks Figural (226–250) | 227–229, 231, 232, 234–239, 242, 245–248, 250 | 12 of 17 |

The classification topic's first cell ("Cari 1 gambar yang berbeda", find the odd one out) is left out of the
picture; the English question text says the same.

**Key cross-check (section B vs section D).** They agree for all 68 imported questions (and for all 250). The script
stops if they ever differ.

**Blind check.** I solved every question from the re-laid images and wrote my answers with a confidence level to
`tools/figural_bank_blind_answers.txt` before comparing. Caveats: while working out the PDF's structure I printed the
start of section D (keys 1–160) to the terminal once, and I saw the "Submateri" line (e.g. `"rotate90+hatch"`) of a
few analogy questions; I didn't use either. Result: **every question I answered with a single letter matches the
key (43 of 43). No question is disputed.** The two "disagreements" (bank 11 and 21) are cases I had already marked
ambiguous, and the key picks the other option of the pair. For bank 34, 39, 45 and 50 (later restored, see below) my
blind answer was "ambiguous" with two candidates, and the key is one of them; for 40 my blind answer (A) matches the key.

**Ambiguity check: 20 questions dropped** (`answerSource: "dropped"`, `verifiedAnswer: null`, flag `ambiguous`, key kept
in `answer`). They are shown with an "Ambiguous, not scored" note, are left out of the mixed set and the wrong-answer
bank, and the results screen counts them as not scored. In every case the source key is one of the options that fit.

| Bank | Subtest | Key | Why |
|---|---|---|---|
| 11 | L6 | C | The example (square → cross-hatched square) can't show a 90° turn. Hatched upright star (B) and hatched turned star (C) both fit |
| 21 | L6 | B | Same with dots: upright dotted star (A) and turned dotted star (B) both fit |
| 33 | L7 | D | Conflicting rules: A is the only shaded figure, but the source key is D based on even/odd sides |
| 51, 60, 61, 64 | L8 | D, A, D, D | Fill cycles plain → hatched → cross-hatched, so the answer is hatched, but two options are the same hatched figure (A=D, A=B, B=D, A=D) |
| 52, 54 | L8 | B, B | A square turning 30° a step repeats every 90°, so the answer looks like figure 2; two options are that same square (B=C, A=B) |
| 55, 56, 57 | L8 | D, A, C | Cycle "one plain, two hatched, three cross-hatched" → two hatched shapes; two options are the same (C=D, A=B, B=C) |
| 59, 70 | L8 | C, A | Arrow grows each step; the two bigger arrows are the same (C=D 169/170 px, A=B) |
| 71 | L8 | B | Count 1, 2, 3, 4 → 5, but no option has 5 shapes; B, C and D are the same four diamonds |
| 229, 246 | L9 | C, D | Answer is a hatched diamond (turning it shows nothing); two options are the same (A=C, A=D) |
| 231 | L9 | C | Medium hatched circle; B and C the same |
| 236 | L9 | A | Medium hatched diamond; A and B the same |
| 238 | L9 | C | Hatched cross (a 90°/180° turn shows nothing); A and C the same |

"Same" was checked by zooming the two options side by side: they differ only in where the hatch lines start. A
pixel comparison doesn't catch this reliably because the hatch position shifts, so I relied on the zoomed view.

**Odd one out (L7), editorial decision: "the only curved figure" is not treated as a competing rule.** In the first
pass I also dropped bank **34, 39, 40, 45 and 50**, because in each a circle is the only curved figure and competes
with the key's rule. By editorial decision these five are **restored and scored with the source key**, which follows
the PDF's structural rules (symmetry / orientation, odd/even sides) rather than the curved-shape distractor:

| Bank | Key | Key's figure | Curved-shape distractor (no longer a reason to drop) |
|---|---|---|---|
| 34 | A | Triangle pointing right: the only odd-sided figure | B, the circle |
| 39 | C | Triangle pointing down: the only odd-sided / pointing-down figure | B, the circle |
| 40 | A | Tilted arrow: the only tilted, odd-sided figure | D, the circle |
| 45 | B | Tilted cross: the only tilted figure (A and D are the same star) | C, the circle |
| 50 | A | Triangle: the only odd-sided figure (B and C are the same square) | D, the circle |

This also settles bank 29 and 44 (count rule, with a lone circle): scored, as before. **Bank 33 stays dropped**: there
the competing rule is fill (A is the only shaded figure), not a curved shape, and the key's D rests on even/odd sides.
L7 now has 16 scored questions and 1 dropped (33).

**Kept and scored, but note:**
- **16, 19** (L6): two wrong options are the same drawing (16: B=C, 19: A=B). The answer D is still the only one that fits.
- **42** (L7): B and C are the same hexagon; D is still the only tilted figure.
- **68, 72** (L8): circles grow by ~20 px a step (83, 102, 123, 142 px). The right option is 163 px; the "too big" one is
  172–173 px. Measurable, but hard to see by eye.
- **12** (L6): the example is a diamond getting bigger and hatched. B is the only big hatched star, but it is also turned,
  which the diamond can't show (the source's rule is "rotate90+hatch+scale"). Kept because no other option fits at all.

**Explanations.** The PDF's section E explanations are templates and were not used. A one-line explanation is
written for 42 of the 48 scored questions. **Empty: bank 12** (the turn in the answer isn't shown by the example, so I
can't state the rule with certainty) and **bank 34, 39, 40, 45, 50** (restored by decision; the source's rule label is
"orientasi simetris" or odd/even sides, and I can't state the exact symmetry rule for each with certainty). The 20
dropped questions have no explanation; their flag note says why.

### Least sure (figural bank)
1. **34, 39, 45, 50** (L7, restored and scored with the key): a test-taker who picks the lone circle is marked wrong.
   40 is less of a worry (A differs on several attributes).
2. **29** and **44** (L7, scored A / B): count rule is clear, but B (29) and C (44) are the only curved figures.
3. **33** (L7, dropped, key D): A being the only shaded figure is arguably the *more* obvious answer than the key's parity rule.
4. **12** (L6, scored B): answer is turned; the example can't show that turn.
5. **68** (L8, scored D): C and D differ by ~6% in size.
6. **72** (L8, scored A): same as 68 (A vs B).
7. **42** (L7, scored D): rests on tilt alone.
8. **53** (L8, scored A): A and D are both big arrows pointing up-left, about 120° vs 150°.
9. **20** (L6, scored C): C and A are both cross-hatched triangles; only the 180° turn separates them.
10. **248** (L9, scored B): D is the same hatched square turned 45°; relies on the matrix only using 90° turns.

## Logic Subtest 10: Figural mix (imported from figural-tests.pdf)

16 picture questions from `figural-tests.pdf` (3 pages; not committed, ignored by `/*.pdf`; no full-page renders
committed). Built by `python tools/import_figural_tests.py`, which reuses `GAP` and `save_image` from
`import_figural_bank.py`. All review decisions live in the script's tables (`AMBIGUOUS`, `DISPUTED`, `OVERRIDES`, `EXPLANATIONS`),
so re-running it keeps them. One subtest, **L10**, with source no. 1–16 in source order. Each question has
`"source": "imported"`, the "Imported, key from source" label, a "Source no. N" label (`sourceRef`), and its `topic`
(analogy / odd one out / series), which the results review shows as a chip. Timer: 16 minutes
(`FIGURAL_TESTS_MINUTES` in `site/js/data.js`).

| Source no. | Topic (page 2 heading) | Options |
|---|---|---|
| 1–4 | analogy (Analogi Gambar) | A–E |
| 5–7 | odd one out (Ketidaksamaan Gambar) | A–E |
| 8–11 | series (Serial) | A–E |
| 12–16 | series (no heading, "Lengkapilah pola"; `@belajarbro_id` watermark) | A–D, 14: A–E |

**Images.** Page 1 has one embedded JPEG per question (336–777 px wide). The script takes those from **page 1 only**
(pages 2–3 carry the worked answers). Each image already has the stimulus row on top and the options row below, with
at most five cells a row, which is the layout `import_figural_bank.py` re-lays its strips into. So the images are
not re-laid, only given a white margin and reduced to a 64-colour PNG (`site/img/figtests-NN.png`). The watermarks on
12–16 are kept as they are. At 375 px the exam and the results review have no horizontal scroll. The review's
header row now wraps (`.review-head` in `style.css`) so the extra topic chip fits.

**Duplicates.** Perceptual hash (8×8 DCT) of all 16 images against the 120 images in `site/img`: the closest distance
is 10/64 bits (q04 vs figbank-011, a different puzzle when compared by eye), the rest 14–24. No duplicates with L5–L9.

**Key.** Read from the "Jawaban" lines on pages 2 (no. 1–11) and 3 (no. 12–16, numbered 1–5 there). **The key exists
only once per question, so there is no second copy to cross-check it against.** Key for no. 15 is hedged in the
source ("Sepertinya B, ada ide lain?", "probably B, any other idea?").

**Blind check.** While inspecting the PDF's structure in phase 1 I viewed pages 2–3, so I had seen the key. The blind
answers were therefore made by a separate subagent that only got the 16 page-1 images and a neutral question text per
topic (no key, no explanations, no page 2–3). It wrote `tools/figural_tests_blind_answers.txt` (answer, confidence,
reasoning) before anything was compared. Result: 13 of 16 match the key. Differences: **1** (blind B, key C),
**4** (blind A, key B), **8** (blind B, key D). The comparison and every decision below were checked by zooming into
the images.

**Ambiguity check: 4 dropped** (`answerSource: "dropped"`, `verifiedAnswer: null`, flag `ambiguous`, key kept in
`answer`):

| No. | Key | Why |
|---|---|---|
| 1 | C | The rule gives a two-line ">" with two dots; no option has that. A and C are the same drawing (a three-line arrow with two dots; they differ by 54 px of JPEG noise, different options by 142+ px) |
| 4 | B | Each tile's change from 1 to 2 fits both a 90° turn and a diagonal flip; on figure 3 the turn gives A, the flip gives B |
| 11 | A | Next is ↑ top, rectangle bottom and a *new* symbol on the right: A (S) and B (=) both fit |
| 15 | B | Source key hedged; the blind check found B only with medium confidence (rule: dropped unless an independent high-confidence B) |

**Key overridden: 1.** **8** (source key D, **scored B** by review decision: `verifiedAnswer: "B"`,
`answerSource: "recomputed"`, flag `recomputed`, source key kept in `answer`; `OVERRIDES` table in the script). Every
symbol moves one side anticlockwise each step, and figure 5 repeats figure 1. The black dot goes out, out, in, out,
out, so next it is inside on the lower left: B, the blind answer. D puts the black dot at the upper right and the
white circle outside on the lower left. That breaks the anticlockwise movement, and it also breaks the source's own
explanation, where the white circle alternates in/out. First imported as "disputed" and scored with D, then
overridden to B. (If the dot instead repeated every 4 steps, as the other symbols do, figure 6 would equal figure 2,
which isn't offered; B is the only option that fits any reading.) No question is left disputed.

**Kept and scored, but note:**
- **16** (key B, blind B low): the top box shows what the bottom-left box showed one step earlier, and each box steps
  through 1–3 straight lines, empty, 1–3 wavy lines. B is the only option whose top and bottom-left fit. Its
  bottom-right (1 wavy line) fits only if that box cycles through the wavy states. C and D are the same drawing, but
  both are wrong on the top box.
- **6** (key E): the deciding arrowheads are a few pixels wide; zoomed, C's points clockwise like A, B and D.

**Explanations.** The PDF's explanations were not copied. A one-line explanation is written for 7 of the 12 scored
questions (2, 3, 5, 6, 12, 13, 14). **Empty: 7** (the key's symmetry rule; I can't state exactly which symmetry each
figure has), **9** (the arrow's path is clear, but I can't state the triangle's rule with certainty), **10** (the
figure is built up two strokes a step, but I can't state exactly which strokes come next), **16** (see above), and
**8** (key overridden; its flag note gives the rule). The 4 dropped questions have no explanation; their flag note says why.

### Least sure (figural-tests.pdf)
1. **8** (scored B, source key D overridden): B rests on reading the black dot's in/out pattern as repeating every 3 steps.
2. **16** (scored B): bottom-right box only fits if it cycles through the wavy states; C = D.
3. **15** (dropped, key B): B is plausible; dropped only because the source itself hedges.
4. **4** (dropped, key B): the turn vs flip reading. A test maker would likely mean one of them.
5. **10** (scored A): the build-up rule is plausible, not proven.
6. **9** (scored E): the arrow rule alone leaves C, D and E; E rests on the triangle, whose rule is unclear.
7. **7** (scored C): symmetry judged on small low-resolution figures.
8. **11** (dropped, key A): A and B differ only in the new symbol.
9. **1** (dropped, key C): no option is exactly right.
10. **6** (scored E): tiny arrowheads decide it.

## Logic Subtests 11–16: more sequences, analogies and syllogisms

Written for this site in `tools/gen_logic.py` (same file and format as L1, L3 and L4), which now also writes
`site/data/logic-11..16.json`. Fix a question there and rerun `python tools/gen_logic.py`. The run is seeded and still
produces L1–L4 (and the L2 pictures) byte-identical to before.

| Subtest | Name | Questions | Timer | Easy / medium / hard |
|---|---|---|---|---|
| L11 | Number sequences 2 | 15 | 10 min (as L1) | 5 / 7 / 3 |
| L12 | Number sequences 3 | 15 | 10 min | 4 / 8 / 3 |
| L13 | Analogies 2 | 15 | 8 min (as L3) | 5 / 7 / 3 |
| L14 | Analogies 3 | 15 | 8 min | 4 / 8 / 3 |
| L15 | Syllogisms 2 | 15 | 12 min (as L4) | 5 / 7 / 3 |
| L16 | Syllogisms 3 | 15 | 12 min | 4 / 8 / 3 |

Each question has a `difficulty`. The third set of each topic swaps one easy question for a medium one and uses
harder rules within each level (L12: tribonacci, alternating operations with a missing middle term, 1 − 1/2ⁿ; L16:
five 3-statement questions against two in L15). Every question has its own explanation: the rule, the relation and
why the tempting option fails, or why the conclusion follows and why the others don't. The timers are in
`testMinutes` in `site/js/data.js` and in each JSON's `timeLimitSec`; `check_data.py` checks that they agree.

**Content.**
- *Sequences:* arithmetic and geometric, second differences, two interleaved series, alternating operations
  (× 2 + 3, × 3 − 2, + 5 × 2), squares, cubes, n(n + 1), primes and doubled primes, Fibonacci-like and tribonacci,
  and fractions (n/(n+1), n/(n+2) in lowest terms, × 2/3, 1 − 1/2ⁿ). 9 of the 30 ask for a **missing middle term**
  ("What number is missing?").
- *Analogies:* the same "A : B = C : ?" format as L3. The relations are antonym, synonym, part-whole, cause-effect
  (plus one effect-cause), category-member, tool-user, degree, function and sequence, with only everyday words.
- *Syllogisms:* the same format as L4 (options A–D are conclusions and E is "None of these conclusions follows"). Each
  set has 3 "none follows" questions and mixes all / no / some / some…not. Negative conclusions ("No …", "Some … are
  not …", and in L16-Q15 "It is not true that all …") are the key in 17 of the 24 questions that have one.

**Logic convention (the same as L4).** L4's checker assumes that **every group named in a question has at least one
member** (existential import), so "All A are B" implies "Some A are B". "Some" means at least one, possibly all.
L15–L16 use exactly the same rule. Five keys are valid *only* under it: L15-Q13, L16-Q06, L16-Q08, L16-Q09 and L16-Q15
(checked by re-running the brute force with empty groups allowed). Their explanations say "there is at least one …".

**Checks in code (they run on every build and stop it with an error).**
- *Sequences:* each answer is computed from the rule that builds the sequence. The generator checks that exactly one
  option has that value, and that **no rival rule fits the sequence with any wrong option filled in**. The rival rules
  are constant 1st, 2nd and 3rd differences (polynomials up to degree 3), a constant ratio, "m × previous + c",
  two alternating +k or ×k operations, two interleaved arithmetic or geometric series, p × previous + q × the one before,
  tribonacci, consecutive primes × 1–3 ± 10, n², n³, 2ⁿ and n(n + 1) ± a constant, and for fractions, numerator and
  denominator rules. A rival rule only counts if it is over-determined (fits at least two terms it didn't need), so it
  can't fit by accident. A self-test makes sure the detectors fire on known patterns. They recognise 29 of the 30
  intended rules; the odd one out is L11-Q15, whose n/(n+2) is hidden by lowest terms and was checked by hand. Also
  checked: no run of 4 terms is repeated from L1 or between the new sets, and the correct value's rank among the 5
  options is spread evenly (3 × smallest, 3 × second, … 3 × largest), so it isn't always the middle value.
- *Syllogisms:* every arrangement of the groups (every set of non-empty Venn regions with no group empty: 109 for
  3 groups, 32,297 for 4) is tried. The key must hold in every arrangement where the statements hold, and **every
  wrong option must fail in at least one**. For a "none follows" question, all four must fail. No two options may
  mean the same, no option may repeat a statement, and no statement set may repeat L4.
- *All six sets:* 15 questions, 5 options, A–E the answer 3 times each (L1 and L4 are lopsided), the difficulty
  mix, the correct option the unique longest in at most 3 of 15 (actual: L13 3, L14 1, the others 0), no key form
  in more than half the syllogisms, and no empty explanation.

**What the checks caught.**
1. L15-Q05 offered "Some organisers are paid staff" *and* "Some paid staff are organisers", which mean the same
   (the equivalence check). One was replaced.
2. The length check failed for L15 (4) and L16 (6): "Some … are not …" keys are naturally the longest sentences.
   The distractors were rebalanced so each such key has an equally long distractor, e.g. the reverse "Some … are not …".
   "It is not true that all …" distractors were added to three questions (L15-Q04, L16-Q11, L16-Q15), where
   the fixed E option would otherwise have been the longest.
3. While checking the output I found a bug of my own: the syllogism data had 4 wrong conclusions for questions with a
   key, and E then overwrote one of them. The data now has 3 (4 for "none follows"), and the generator asserts it.
4. No sequence distractor was rejected by the rival-rule check: the wrong options were hand-picked slips (repeating
   the last step, the wrong one of two series, the wrong operation, averaging the neighbours).

**Blind check.** A fresh subagent answered all 90 questions from a copy without keys, explanations or relations,
and named the relation of each analogy (`tools/logic_tpa_blind_answers.txt`). It agreed with **90/90** keys and with
all 30 relation labels. It raised two doubts, and I rewrote both:

| Question | Doubt | Change |
|---|---|---|
| L14-Q06 Umbrella : Rain = Helmet : **Injury** | "Head" defensible as "what it protects" | Distractor "Head" replaced by "Strap"; explanation updated |
| L14-Q15 Anchor : Ship = Brake : **Car** | A brake is also *part of* a car, so the relation reads two ways (and "Wheel" gets close) | Rewritten as Anchor : Ship = Leash : **Dog** (holds in place), with Owner / Walk / Park / Rope |

A second fresh subagent answered the two rewritten questions blind and found both clean (D and B, "function", no
second defensible option). I also extended the explanations of L15-Q04 and L16-Q11 to cover their "It is not true
that …" option, which a test answer during the browser check showed was missing.

**Site check.** `check_data.py` has new checks for L11–L16: 15 questions, the difficulty mix, A–E 3 each, the
length giveaway, a relation on every analogy, "None of these conclusions follows." as option E on every syllogism,
the `data.js` timers matching the JSON, and no repeated question across L1–L4 and L11–L16. In Chrome I ran a full L15
exam (15 answers, 3 wrong on purpose): 12/15, 12:00 timer, the 3 wrong answers in the wrong-answer bank, and the
review filter works. I also ran L13 (8:00) and viewed its results review at 375 px, with no horizontal scroll. The test
attempts were removed and the saved progress restored exactly.

### Least sure (L11–L16)
| Question | Issue |
|---|---|
| L14-Q06 | Helmet : **Injury** ("protects against"). Rewritten after the blind pass; the abstract answer may still feel less natural than a concrete one. |
| L14-Q15 | Leash : **Dog**. New after the blind pass and checked by one subagent only. "Owner" is the tempting wrong answer. |
| L13-Q15 | Ruler : Length = Clock : **Time** ("measures"). "Hour" (a unit) and "Watch" (another clock) are deliberate traps; labelled "function". |
| L15-Q13 | "All nurses are shift workers; all nurses are first-aiders → some shift workers are first-aiders." Valid **only** under the at-least-one-member convention, the same as L4. Under modern logic, E would be the answer. |
| L11-Q15 | 1/3, 1/2, 3/5, 2/3 → **5/7** (n/(n+2) with 2/4 and 4/6 reduced). The only intended rule the rival-rule detectors don't recognise, so it was checked by hand; it is hard because the pattern is hidden by lowest terms. |
