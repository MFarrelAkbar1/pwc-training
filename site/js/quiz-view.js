// The question screen, for both exam mode (timed, answers revealed at the end)
// and practice mode (untimed, feedback after each answer).
import { el, clear, showModal, closeModals, formatTime } from "./dom.js";
import { correctAnswer, sectionOf } from "./data.js";
import { createQuiz, buildAttempt, secondsLeft, elapsedSeconds } from "./quiz.js";
import { renderContext, contextKey, contextTitle, sourceLabel, renderOptions, renderAnswerReview, renderFlag,
  renderGenerated, renderQuestionImage } from "./render.js";
import { destroyCharts } from "./charts.js";
import { recordAttempt } from "./storage.js";

let quiz = null; // the running quiz
let view = null; // DOM nodes we update
let timerId = null;

export function isQuizRunning() {
  return quiz !== null && quiz.finishedAt === null;
}

export function stopQuiz() {
  clearInterval(timerId);
  timerId = null;
  document.removeEventListener("keydown", onKey);
  window.removeEventListener("beforeunload", onBeforeUnload);
  closeModals();
  destroyCharts();
  quiz = null;
  view = null;
}

export function startQuiz(app, options) {
  stopQuiz();
  quiz = createQuiz(options);
  clear(app);
  view = buildLayout();
  app.append(view.root);
  document.addEventListener("keydown", onKey);
  window.addEventListener("beforeunload", onBeforeUnload);
  tick();
  timerId = setInterval(tick, 250);
  show(0);
}

const current = () => quiz.questions[quiz.index];

// ---------- layout ----------

function buildLayout() {
  const isExam = quiz.mode === "exam";
  const timer = el("span", { class: "timer", title: isExam ? "Time left" : "Time spent" });
  const header = el("header", { class: "quiz-bar" },
    el("div", { class: "quiz-title" },
      el("strong", {}, quiz.set.title),
      el("span", { class: `chip ${quiz.mode}` }, isExam ? "Exam" : "Practice")),
    el("div", { class: "quiz-actions" },
      timer,
      isExam && el("button", { class: "btn primary", onclick: confirmSubmit }, "Submit"),
      el("button", { class: "btn", onclick: () => { location.hash = `#/section/${quiz.set.section}`; } }, "Quit")));

  const context = el("div", { class: "context-body" });
  const contextTitle = el("summary", {});
  const contextBox = el("details", { class: "context", open: true }, contextTitle, context);
  const question = el("section", { class: "question-panel", "aria-live": "polite" });
  const navigator = el("nav", { class: "navigator", "aria-label": "Question navigator" });

  const body = el("div", { class: "quiz-body" },
    el("aside", { class: "context-panel" }, contextBox),
    el("div", { class: "question-col" }, question, navigator));
  const root = el("div", { class: "quiz" }, header, body);
  return { root, body, timer, context, contextBox, contextTitle, question, navigator, contextKey: undefined };
}

// ---------- drawing ----------

function show(index) {
  quiz.index = index;
  const q = current();
  // Only redraw the chart/passage when it changes, so it doesn't flicker between questions.
  const key = contextKey(q); // null when the question has no chart or passage
  if (key !== view.contextKey) {
    destroyCharts();
    clear(view.context);
    if (key) {
      renderContext(view.context, q);
      view.contextTitle.textContent = contextTitle(q);
      view.contextBox.open = true;
    }
    view.body.classList.toggle("no-context", !key); // single column when there's nothing to show
    view.contextKey = key;
  }
  drawQuestion();
  drawNavigator();
}

function drawQuestion() {
  const q = current();
  const chosen = quiz.answers[q.id];
  const revealed = quiz.mode === "practice" && chosen != null;
  clear(view.question);
  // (native append prints null/false as text, so the optional parts are filtered out first)
  view.question.append(...[
    el("div", { class: "q-head" },
      el("span", { class: "q-num" }, `Question ${quiz.index + 1} of ${quiz.questions.length}`),
      quiz.set.kind !== "test" && el("span", { class: "source" }, sourceLabel(q)),
      renderGenerated(q),
      quiz.marked.has(q.id) && el("span", { class: "chip marked" }, "Marked for review")),
    renderFlag(q, revealed),
    el("p", { class: "q-text" }, q.text),
    renderQuestionImage(q),
    sectionOf(q) === "numerical" &&
      el("p", { class: "hint" }, "Estimate first, then calculate. Rule out options that are clearly too big or too small."),
    renderOptions(q, { chosen, revealed, onPick: pick }),
    revealed && renderAnswerReview(q, chosen),
    navButtons(),
  ].filter(Boolean));
}

function navButtons() {
  const q = current();
  const i = quiz.index;
  const isExam = quiz.mode === "exam";
  const isLast = i === quiz.questions.length - 1;
  const answered = quiz.answers[q.id] != null;
  return el("div", { class: "q-nav" },
    el("button", { class: "btn", disabled: i === 0, onclick: () => show(i - 1) }, "← Previous"),
    isExam && el("button", { class: "btn" + (quiz.marked.has(q.id) ? " active" : ""), onclick: toggleMark },
      quiz.marked.has(q.id) ? "Unmark" : "Mark for review"),
    isLast
      ? el("button", { class: "btn primary", onclick: confirmSubmit }, isExam ? "Submit" : "Finish")
      : el("button", { class: "btn primary", onclick: () => show(i + 1) }, answered ? "Next →" : "Skip →"));
}

function drawNavigator() {
  const answeredCount = Object.keys(quiz.answers).length;
  const summary = `${answeredCount} of ${quiz.questions.length} answered` +
    (quiz.mode === "exam" ? ` · ${quiz.marked.size} marked for review` : "");
  clear(view.navigator);
  view.navigator.append(
    el("p", { class: "nav-summary" }, summary),
    el("div", { class: "nav-grid" }, ...quiz.questions.map((q, i) => {
      const chosen = quiz.answers[q.id];
      const classes = ["nav-btn"];
      if (chosen != null) classes.push("answered");
      if (quiz.mode === "practice" && chosen != null && correctAnswer(q) != null) {
        classes.push(chosen === correctAnswer(q) ? "right" : "wrong");
      }
      if (quiz.marked.has(q.id)) classes.push("marked");
      if (i === quiz.index) classes.push("current");
      return el("button", {
        class: classes.join(" "),
        "aria-label": `Question ${i + 1}${chosen != null ? ", answered" : ""}${quiz.marked.has(q.id) ? ", marked" : ""}`,
        "aria-current": i === quiz.index ? "step" : null,
        onclick: () => show(i),
      }, String(i + 1));
    })));
}

// ---------- actions ----------

function pick(letter) {
  const q = current();
  if (quiz.mode === "practice" && quiz.answers[q.id] != null) return; // practice answers lock once given
  quiz.answers[q.id] = letter;
  drawQuestion();
  drawNavigator();
}

function toggleMark() {
  const id = current().id;
  if (quiz.marked.has(id)) quiz.marked.delete(id);
  else quiz.marked.add(id);
  drawQuestion();
  drawNavigator();
}

function confirmSubmit() {
  const unanswered = quiz.questions.length - Object.keys(quiz.answers).length;
  const notes = [];
  if (unanswered) notes.push(`${unanswered} unanswered`);
  if (quiz.marked.size) notes.push(`${quiz.marked.size} marked for review`);
  showModal({
    title: quiz.mode === "exam" ? "Submit your answers?" : "Finish practice?",
    body: notes.length
      ? `You have ${notes.join(" and ")}. Unanswered questions count as wrong.`
      : "You've answered every question.",
    confirmText: quiz.mode === "exam" ? "Submit" : "Finish",
    cancelText: "Back to the test",
    onConfirm: () => finish(false),
  });
}

function finish(timeRanOut) {
  if (!isQuizRunning()) return;
  quiz.finishedAt = timeRanOut ? quiz.endsAt : Date.now();
  quiz.autoSubmitted = timeRanOut;
  const attempt = buildAttempt(quiz);
  recordAttempt(attempt);
  stopQuiz();
  location.hash = `#/results/${attempt.id}`;
}

function tick() {
  if (quiz.mode === "exam") {
    const left = secondsLeft(quiz);
    view.timer.textContent = `⏱ ${formatTime(left)}`;
    view.timer.classList.toggle("low", left <= 120);
    if (left === 0) finish(true);
  } else {
    view.timer.textContent = `⏱ ${formatTime(elapsedSeconds(quiz))}`;
  }
}

// Keys: A–E or 1–5 choose an answer, ← / → move between questions.
function onKey(e) {
  if (e.altKey || e.ctrlKey || e.metaKey || document.querySelector(".modal-overlay")) return;
  const letters = Object.keys(current().options);
  const byLetter = letters.indexOf(e.key.toUpperCase());
  const byNumber = e.key.length === 1 ? "12345".indexOf(e.key) : -1;
  const choice = byLetter >= 0 ? byLetter : byNumber;
  if (choice >= 0 && choice < letters.length) {
    pick(letters[choice]);
  } else if (e.key === "ArrowRight" && quiz.index < quiz.questions.length - 1) {
    show(quiz.index + 1);
  } else if (e.key === "ArrowLeft" && quiz.index > 0) {
    show(quiz.index - 1);
  } else {
    return;
  }
  e.preventDefault();
}

function onBeforeUnload(e) {
  e.preventDefault();
  e.returnValue = ""; // asks the browser to confirm closing/reloading mid-test
}
