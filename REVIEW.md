# Review: problems found in the source PDF

Nothing from the PDF is overwritten. Every question keeps the PDF key in `answer`.
When there's a problem, the question also gets:

| Field | Meaning |
|---|---|
| `verifiedAnswer` | The answer the site scores against (`null` = not scored) |
| `answerSource` | `"recomputed"` (my answer replaces the PDF key) or `"dropped"` (no option is correct) |
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
| N1-Q19 | B | — | dropped |
| N2-Q02 | E | **D** | recomputed |
| N2-Q07 | B | B | disputed |
| N2-Q11 | B | B | disputed (typo in question) |
| N2-Q17 | B | **A** | recomputed |
| N3-Q01 | C | C | disputed |
| N3-Q04 | B | **E** | disputed, uses E (your decision) |
| N3-Q08 | D | **E** | recomputed |

In total: 6 recomputed, 1 dropped (N1-Q19), 3 disputed with the PDF key kept, and 1 disputed using my answer (N3-Q04). Tests 4 and 5 have no key problems.

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
| V2-Q11 | Cannot say | True | **True** | recomputed (your decision) | medium |
| V2-Q13 | True | Cannot say | True | disputed | low |
| V2-Q15 | False | Cannot say | False | disputed | low |
| V3-Q01 | *none* | Cannot say | **Cannot say** | no key in source (my judgment, confirmed) | high |
| V3-Q07 | Cannot say | Cannot say | Cannot say | truncated | — (agree) |
| V3-Q09 | True | Cannot say | **Cannot say** | recomputed (your decision) | medium |
| V3-Q12 | True | Cannot say* | True | truncated | — (*from visible text only) |
| V4-Q05 | True | **False** | **False** | recomputed (confirmed) | high |
| V4-Q06 | False | **True** | **True** | recomputed (confirmed) | high |
| V4-Q09 | Cannot say | Cannot say | Cannot say | truncated | — (agree) |
| V4-Q15 | Cannot say | Cannot say | Cannot say | truncated | — (agree) |
| V6-Q14 | True | Cannot say | True | disputed | medium |
| V7-Q06 | Cannot say | True | **True** | recomputed (your decision) | low |
| V7-Q14 | False | Cannot say | False | disputed | medium |

**After your decisions:** 7 recomputed (the 2 switches plus 5 where you chose my answer), 5 disputed with the PDF key kept (V2-Q02, V2-Q13, V2-Q15, V6-Q14, V7-Q14), 1 with no key in source, and 5 truncated with the PDF key kept (V3-Q12 stays True).

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
