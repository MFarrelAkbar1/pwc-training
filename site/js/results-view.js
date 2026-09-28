// Results screen: score, time used, and a review of every question.
// The tests the questions came from must be loaded first (app.js does this).
import { el, clear, formatTime } from "./dom.js";
import { findQuestion } from "./data.js";
import { renderContext, hasContext, contextTitle, sourceLabel, renderOptions, renderAnswerReview,
  renderFlag, renderGenerated, renderSourceRef, renderTopic, renderQuestionImage } from "./render.js";

const FILTERS = { all: "All questions", wrong: "Wrong or unanswered", flagged: "Flagged in source" };

// Buttons for trying again, depending on what kind of set this was.
function retryLinks(attempt) {
  if (attempt.kind === "mixed") {
    return [
      el("a", { class: "btn primary", href: `#/mixed/${attempt.section}/exam` }, "New mixed set (exam)"),
      el("a", { class: "btn", href: `#/mixed/${attempt.section}/practice` }, "New mixed set (practice)"),
    ];
  }
  if (attempt.kind === "redo") {
    return [el("a", { class: "btn primary", href: `#/redo/${attempt.section}` }, "Redo wrong answers again")];
  }
  return [
    el("a", { class: "btn primary", href: `#/quiz/${attempt.testId}/exam` }, "Retake as exam"),
    el("a", { class: "btn", href: `#/quiz/${attempt.testId}/practice` }, "Practice mode"),
  ];
}

export function showResults(app, attempt) {
  clear(app);
  const pct = attempt.total ? Math.round((attempt.score / attempt.total) * 100) : 0;
  const notScored = attempt.results.filter((r) => !r.scored).length;
  const isExam = attempt.mode === "exam";
  const showSource = attempt.kind !== "test";

  const list = el("ol", { class: "review-list" });
  const filterButtons = Object.entries(FILTERS).map(([key, label]) =>
    el("button", { class: "btn small", "data-filter": key, onclick: () => drawList(key) }, label));

  function drawList(filter) {
    filterButtons.forEach((b) => b.classList.toggle("active", b.dataset.filter === filter));
    clear(list);
    attempt.results.forEach((r, i) => {
      const q = findQuestion(r.id);
      if (!q) return;
      if (filter === "wrong" && (!r.scored || r.isCorrect)) return;
      if (filter === "flagged" && !q.flag) return;
      list.append(reviewItem(q, r, i + 1, showSource));
    });
    if (!list.children.length) list.append(el("li", { class: "muted" }, "No questions match this filter."));
  }

  app.append(
    el("a", { class: "back", href: `#/section/${attempt.section}` }, "← Back to tests"),
    el("section", { class: "score-card" },
      el("p", { class: "muted" }, `${attempt.title} · ${isExam ? "Exam" : "Practice"} mode`),
      el("p", { class: "score" }, `${attempt.score} / ${attempt.total}`, el("span", { class: "pct" }, ` ${pct}%`)),
      el("p", {}, isExam
        ? `Time used: ${formatTime(attempt.timeUsedSec)} of ${formatTime(attempt.timeLimitSec)}`
        : `Time spent: ${formatTime(attempt.timeUsedSec)}`),
      attempt.autoSubmitted && el("p", { class: "flag" }, "Time ran out, so your answers were submitted automatically."),
      notScored > 0 && el("p", { class: "muted" },
        `${notScored} question${notScored > 1 ? "s aren't" : " isn't"} scored because the source has no single correct option ` +
        "(none is correct, or the question is ambiguous). See the \"Flagged in source\" filter."),
      el("p", { class: "muted" }, attempt.kind === "redo"
        ? "A question leaves your wrong-answer bank after you get it right twice in a row."
        : "Questions you got wrong are saved to your wrong-answer bank."),
      el("div", { class: "actions" }, ...retryLinks(attempt), el("a", { class: "btn", href: "#/" }, "Home"))),
    el("h2", {}, "Review"),
    el("div", { class: "filters", role: "group", "aria-label": "Filter questions" }, ...filterButtons),
    list);
  drawList("all");
}

function reviewItem(q, r, number, showSource) {
  const [tone, label] = !r.scored ? ["neutral", "Not scored"]
    : r.chosen == null ? ["bad", "Not answered"]
    : r.isCorrect ? ["good", "Correct"] : ["bad", "Wrong"];
  // The chart/passage is only drawn when you open it.
  const context = hasContext(q) // null (not false) when there's nothing to show, so ?. below works
    ? el("details", { class: "review-context" }, el("summary", {}, `Show ${contextTitle(q).toLowerCase()}`))
    : null;
  context?.addEventListener("toggle", () => {
    if (context.open && !context.dataset.drawn) {
      context.dataset.drawn = "yes";
      const body = el("div", { class: "context-body" });
      context.append(body);
      renderContext(body, q);
    }
  });

  return el("li", { class: `review-item status-${tone}` },
    el("div", { class: "review-head" },
      el("span", { class: "q-num" }, `Question ${number}`),
      showSource && el("span", { class: "source" }, sourceLabel(q)),
      renderGenerated(q),
      renderSourceRef(q),
      renderTopic(q),
      el("span", { class: `badge ${tone}` }, label)),
    el("p", { class: "q-text" }, q.text),
    renderQuestionImage(q),
    renderOptions(q, { chosen: r.chosen, revealed: true }),
    renderAnswerReview(q, r.chosen),
    renderFlag(q, true),
    context);
}
