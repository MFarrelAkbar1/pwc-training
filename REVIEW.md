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

These 180 questions were **written for this site**, not taken from the PDF. Every one has
`"source": "generated"` and shows a "Generated · unverified" label. The section pages say that
the questions haven't been checked against an official source.

| Section | Tests | Questions | Timer | How answers were produced |
|---|---|---|---|---|
| English (TOEFL-style) | E1–E3 | 3 × 20 (8 sentence completion, 4 error spotting, 8 reading from 2 passages) | 15 min each | Written and checked by hand |
| Logic (TPA-style) | L1–L4 | 4 × 15 | 10 / 12 / 8 / 12 min | **Computed** by `tools/gen_logic.py` (L1, L2, L4); L3 written by hand |
| Technical (Risk Assurance) | T1–T3 | 3 × 20 (18 of 60 scenario-based; easy, medium and hard mixed) | 20 min each | Written and checked by hand |

Regenerate the Logic tests with `python tools/gen_logic.py` (seeded, so the output is the same each time).
`python tools/check_data.py` checks the structure of all 22 test files.

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
`site/data/logic-5.json`. Every question has `"source": "imported"` and shows an "Imported, key from source" label.
The **scored answer is always the source key** (`jawaban.txt`); where I disagree the question is flagged `disputed`.
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
| 9 | C | C | **low** | Six arcs; I could not find a rule that singles out one option (frame 3 is frame 2 reversed and frame 4 is frame 1 reversed, but that does not give a unique frame 6). C is a guess |
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
They are **empty for Q3, Q4, Q9, Q13** (rule not clear to me) and **Q11** (disputed; the flag note explains instead).

### Least sure (figural)
1. **Q9**: no rule found; my answer is a guess that happens to match the key.
2. **Q13**: B and D both fit the rotate-and-add rule; the key's D is plausible, not proven.
3. **Q3 / Q4**: the big symbol is certain (C or D); the small letter that decides between them is not.
4. **Q11**: the one disagreement; recheck by comparing option A with frame 2.
5. **Q7**: counting lines in small teeth. The 1, 3, 5 progression is my reading of a low-resolution image.
