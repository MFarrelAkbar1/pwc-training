// Pieces of the question screen shared by the quiz and the results review.
import { el, fmt } from "./dom.js";
import { SECTIONS, acceptedAnswers, isAccepted, testOf, testIdOf, sectionOf } from "./data.js";
import { drawChart, chartHeight, describeChart } from "./charts.js";

// ---------- chart / table / passage panel ----------

// Each question brings its own chart/table or passage from the test it belongs to.
// Some questions (grammar, logic, technical) have neither.
export function hasContext(q) {
  return Boolean(q.dataset || q.passage);
}

// A passage can carry its own title (e.g. "Instructions: word swap"); otherwise it's just "Passage".
export function contextTitle(q) {
  if (q.passage) return testOf(q).passages[q.passage].title ?? "Passage";
  return "Chart / table";
}

export function renderContext(container, q) {
  const test = testOf(q);
  if (q.passage) renderPassage(container, test.passages[q.passage]);
  else if (q.dataset) renderDataset(container, test.datasets[q.dataset]);
}

// Identifies the chart/passage a question uses, so the panel is only redrawn when it changes.
export function contextKey(q) {
  return hasContext(q) ? `${testIdOf(q)}:${q.dataset ?? q.passage}` : null;
}

// "Numerical Test 3 · Question 4": where a question in a mixed or redo set comes from.
export function sourceLabel(q) {
  const [test, number] = q.id.split("-");
  return `${SECTIONS[sectionOf(q)].short} Test ${test.slice(1)} · Question ${Number(number.slice(1))}`;
}

// The question sentence. Error-identification questions (English 5 onwards) mark each underlined part as
// {A|text}; those parts are drawn underlined with their letter beneath. Older questions are plain text.
const UNDERLINED_PART = /\{([A-F])\|([^}]*)\}/g;

export function renderQuestionText(q) {
  const text = el("p", { class: "q-text" });
  let last = 0;
  for (const match of q.text.matchAll(UNDERLINED_PART)) {
    text.append(q.text.slice(last, match.index),
      el("span", { class: "ul-part" }, el("u", {}, match[2]), el("span", { class: "ul-letter" }, match[1])));
    last = match.index + match[0].length;
  }
  text.append(q.text.slice(last));
  if (last === 0) return text;
  return el("div", {},
    el("p", { class: "hint" }, "Choose the underlined part that must be changed for the sentence to be correct."),
    text);
}

// The figure for a question that is itself a picture (Logic figure patterns).
// Tapping it toggles a zoomed view that scrolls sideways, for small details on a phone.
export function renderQuestionImage(q) {
  if (!q.image) return null;
  const image = el("img", {
    class: "q-image",
    src: q.image,
    alt: q.imageAlt ?? "Question figure",
    title: "Tap to zoom",
    onclick: () => image.classList.toggle("zoomed"),
  });
  return el("div", { class: "q-image-wrap" }, image);
}

// Small label on questions written for this site rather than taken from the source PDF,
// or imported from an outside source (answer key taken from that source, not checked against an official one).
export function renderGenerated(q) {
  if (q.source === "imported") {
    return el("span", {
      class: "chip imported",
      title: "Imported from an outside question set; the answer key is that source's key.",
    }, "Imported, key from source");
  }
  if (q.source !== "generated") return null;
  return el("span", {
    class: "chip generated",
    title: "This question was generated for practice and hasn't been checked against an official source.",
  }, "Generated · unverified");
}

// The question's number in the outside set it was imported from ("Bank no. 57"), so it can be looked up there.
export function renderSourceRef(q) {
  return q.sourceRef ? el("span", { class: "chip source-ref" }, q.sourceRef) : null;
}

// The question's topic in a mixed imported test ("series"), shown in the results review.
export function renderTopic(q) {
  return q.topic ? el("span", { class: "chip source-ref" }, `Topic: ${q.topic}`) : null;
}

const CUT_MARKER = "[...text cut off in source]";

function renderPassage(container, passage) {
  const cut = passage.text.endsWith(CUT_MARKER);
  const text = cut ? passage.text.slice(0, -CUT_MARKER.length).trimEnd() : passage.text;
  container.append(el("p", { class: "passage" },
    text,
    cut && el("span", { class: "cut-marker" }, " […text cut off in source]")));
}

function renderDataset(container, dataset) {
  container.append(el("h3", { class: "ds-title" }, dataset.title));
  for (const block of dataset.blocks) {
    const figure = el("figure", { class: "block" }, block.title && el("figcaption", {}, block.title));
    container.append(figure);
    if (block.kind === "table") {
      figure.append(renderTable(block));
    } else {
      const canvas = el("canvas", { role: "img", "aria-label": describeChart(block) });
      figure.append(el("div", { class: "chart", style: `height:${chartHeight(block)}px` }, canvas));
      try {
        drawChart(canvas, block);
      } catch (err) {
        figure.append(el("p", { class: "ds-note" }, `${err.message}. Use "Show original" below.`));
      }
    }
    if (block.note) figure.append(el("p", { class: "ds-note" }, block.note));
  }
  const image = el("img", { src: dataset.image, alt: "Original chart from the source PDF", loading: "lazy", hidden: true });
  const toggle = el("button", {
    class: "btn small",
    onclick: () => {
      image.hidden = !image.hidden;
      toggle.textContent = image.hidden ? "Show original from PDF" : "Hide original";
    },
  }, "Show original from PDF");
  container.append(el("div", { class: "original" }, toggle, image));
}

function renderTable(block) {
  return el("div", { class: "table-wrap" },
    el("table", {},
      el("thead", {}, el("tr", {}, ...block.columns.map((c) => el("th", { scope: "col" }, c)))),
      el("tbody", {}, ...block.rows.map((row) =>
        el("tr", {}, el("th", { scope: "row" }, fmt(row[0])), ...row.slice(1).map((v) => el("td", {}, fmt(v))))))));
}

// ---------- answer options ----------

export function optionLabel(q, letter) {
  return `${letter} (${q.options[letter]})`;
}

// revealed = show which option is right/wrong. Without onPick the buttons are read-only.
export function renderOptions(q, { chosen, revealed, onPick }) {
  const accepted = acceptedAnswers(q);
  return el("div", { class: "options", role: "radiogroup", "aria-label": "Answer options" },
    ...Object.entries(q.options).map(([letter, text]) => {
      const classes = ["option"];
      if (letter === chosen) classes.push("selected");
      if (revealed && accepted.length) {
        if (accepted.includes(letter)) classes.push("correct");
        else if (letter === chosen) classes.push("wrong");
      }
      return el("button", {
        class: classes.join(" "),
        role: "radio",
        "aria-checked": String(letter === chosen),
        disabled: revealed || !onPick,
        onclick: () => onPick(letter),
      }, el("span", { class: "letter" }, letter), el("span", { class: "option-text" }, text));
    }));
}

// Verdict + explanation, shown after answering (practice) and on the results screen.
export function renderAnswerReview(q, chosen) {
  const accepted = acceptedAnswers(q);
  const answerText = `Correct answer${accepted.length > 1 ? "s" : ""}: ${accepted.map((l) => optionLabel(q, l)).join(" or ")}`;
  let verdict;
  if (!accepted.length) verdict = el("p", { class: "verdict neutral" }, "Not scored");
  else if (chosen == null) verdict = el("p", { class: "verdict bad" }, `Not answered. ${answerText}`);
  else if (isAccepted(q, chosen)) verdict = el("p", { class: "verdict good" }, "✓ Correct");
  else verdict = el("p", { class: "verdict bad" }, `✗ Your answer: ${optionLabel(q, chosen)}. ${answerText}`);
  return el("div", { class: "review" },
    verdict,
    q.explanation && el("p", { class: "explanation" }, el("strong", {}, "Explanation: "), q.explanation));
}

// ---------- notes on questions with a problem in the source ----------

const FLAGS = {
  recomputed: {
    label: "Answer corrected",
    before: "The source PDF's answer key is wrong here, so this site uses a checked answer. Details after you answer.",
  },
  disputed: {
    label: "Disputed in source",
    before: "The source answer is debatable. Details after you answer.",
  },
  ambiguous: {
    label: "Ambiguous, not scored",
    before: "More than one option fits the rule here (or two options look the same), so this question doesn't count. " +
      "Answer it for practice; details after you answer.",
  },
  dropped: {
    label: "Not scored",
    before: "None of the options is correct in the source, so this question doesn't count. Answer it for practice.",
  },
  "missing-key": {
    label: "No key in source",
    before: "The source PDF gives no answer here; the answer used is a judgment. Details after you answer.",
  },
  truncated: {
    label: "Passage cut off in source",
    before: "Part of the passage is missing in the source PDF. Details after you answer.",
  },
};

// Before answering (exam) only a short warning is shown, so the note can't give the answer away.
export function renderFlag(q, revealed) {
  const type = q.flag?.type;
  if (!type) return null;
  const info = FLAGS[type];
  const box = el("div", { class: `flag flag-${type}` }, el("strong", {}, `⚠ ${info.label}`));
  if (!revealed) {
    box.append(el("p", {}, info.before));
    return box;
  }
  if (q.answer != null && q.answerSource === "recomputed") {
    box.append(el("p", { class: "flag-keys" },
      `Source PDF key: ${optionLabel(q, q.answer)} · This site uses: ${optionLabel(q, q.verifiedAnswer)}`));
  } else if (q.answer != null && q.answerSource === "dropped") {
    box.append(el("p", { class: "flag-keys" }, `Source PDF key: ${optionLabel(q, q.answer)} · Not scored here`));
  }
  box.append(el("p", {}, q.flag.note));
  return box;
}
