// Entry point: a tiny hash router plus the home and test-list screens.
//   #/                          home: sections + progress summary
//   #/section/numerical         tests in a section, mixed set, wrong-answer redo
//   #/quiz/N1/exam              take one test (exam or practice)
//   #/mixed/verbal/exam         a random set from every test in the section
//   #/redo/numerical            redo questions from the wrong-answer bank (practice)
//   #/results/<attempt id>
// Add ?t=10 to a quiz address to shorten the timer to 10 s (a testing aid).
import { el, clear, showModal } from "./dom.js";
import { SECTIONS, testId, isTestId, loadTests, singleTestSet, mixedSet, redoSet } from "./data.js";
import { loadProgress, statsFor, sectionSummary, bankIds, getAttempt, resetProgress } from "./storage.js";
import { startQuiz, stopQuiz, isQuizRunning } from "./quiz-view.js";
import { showResults } from "./results-view.js";
import { destroyCharts } from "./charts.js";

const app = document.getElementById("app");
const MODES = ["exam", "practice"];
let currentHash = location.hash || "#/";

window.addEventListener("hashchange", onHashChange);
route(); // (everything this uses must be declared above this line)

// Leaving a running test (Quit, back button, a link) asks first.
function onHashChange() {
  if (isQuizRunning() && location.hash !== currentHash) {
    const target = location.hash;
    history.replaceState(null, "", currentHash); // stay on the test for now
    showModal({
      title: "Leave this test?",
      body: "Your answers so far won't be saved.",
      confirmText: "Leave test",
      cancelText: "Keep going",
      onConfirm: () => {
        stopQuiz();
        location.hash = target;
      },
    });
    return;
  }
  route();
}

function parseHash() {
  const [path, query = ""] = (location.hash || "#/").slice(1).split("?");
  return { parts: path.split("/").filter(Boolean), params: new URLSearchParams(query) };
}

async function route() {
  currentHash = location.hash || "#/";
  const [page, a, b] = parseHash().parts;
  destroyCharts();
  window.scrollTo(0, 0);
  try {
    if (page === "section" && SECTIONS[a]) return showSection(a);
    if (page === "quiz" && isTestId(a) && MODES.includes(b)) return run(await singleTestSet(a), b);
    if (page === "mixed" && SECTIONS[a] && MODES.includes(b)) return run(await mixedSet(a), b);
    if (page === "redo" && SECTIONS[a]) return openRedo(a);
    if (page === "results") return await openResults(a);
    showHome();
  } catch (err) {
    showError(err);
  }
}

function run(set, mode) {
  const shortTimer = Number(parseHash().params.get("t")); // testing aid: ?t=10
  startQuiz(app, { set, mode, timeLimitSec: shortTimer > 0 ? shortTimer : set.timeLimitSec });
}

// ---------- home ----------

function showHome() {
  clear(app);
  const hasProgress = loadProgress().attempts.length > 0 || Object.keys(loadProgress().wrongBank).length > 0;
  app.append(
    el("header", { class: "page-head" },
      el("h1", {}, "PwC Aptitude Practice"),
      el("p", { class: "muted" },
        "Numerical and verbal reasoning from past PwC test questions, plus generated practice sets for English, " +
        "logic and technical (risk assurance). Exam mode is timed; practice mode explains every answer.")),
    el("div", { class: "cards" }, ...Object.entries(SECTIONS).map(([key, s]) => sectionCard(key, s))),
    el("section", { class: "progress" },
      el("h2", {}, "Your progress"),
      hasProgress
        ? el("div", { class: "table-wrap" }, progressTable())
        : el("p", { class: "muted" }, "No attempts yet. Your scores and missed questions will show up here."),
      el("p", { class: "muted small" }, "Progress is saved in this browser only."),
      hasProgress && el("button", { class: "btn small", onclick: confirmReset }, "Reset progress")));
}

// "4 subtests · 15 questions each · 8–12 minutes"; a range when the tests differ ("6 tests · 15–20 questions · …")
function sectionDetails(section) {
  const perTest = (overrides, fallback) => section.tests.map((n) => overrides?.[n] ?? fallback);
  const span = (values, unit, each) => {
    const [lo, hi] = [Math.min(...values), Math.max(...values)];
    return lo === hi ? `${lo} ${unit}${each ? " each" : ""}` : `${lo}–${hi} ${unit}`;
  };
  const kind = section.testNames ? "subtests" : "tests";
  return `${section.tests.length} ${kind} · ${span(perTest(section.testQuestions, section.questions), "questions", true)}` +
    ` · ${span(perTest(section.testMinutes, section.minutes), "minutes")}`;
}

function sectionCard(key, section) {
  return el("a", { class: "card", href: `#/section/${key}` },
    el("h2", {}, section.name),
    el("p", { class: "muted" }, sectionDetails(section)),
    section.generated
      ? el("p", {}, el("span", { class: "chip generated" }, "Generated · unverified"))
      : el("p", {}, el("span", { class: "chip source-pdf" }, "From past test PDF")),
    el("p", {}, "Tests, mixed sets and wrong-answer redo →"));
}

function progressTable() {
  const row = (key) => {
    const s = sectionSummary(key);
    return el("tr", {},
      el("th", { scope: "row" }, SECTIONS[key].name),
      el("td", {}, String(s.attempts)),
      el("td", {}, `${s.testsTried} of ${SECTIONS[key].tests.length}`),
      el("td", {}, s.bestPct == null ? "–" : `${s.bestPct}% (${s.bestTitle.replace(/^.*– /, "")})`),
      el("td", {}, String(s.bank)));
  };
  return el("table", { class: "progress-table" },
    el("thead", {}, el("tr", {},
      ...["", "Attempts", "Tests tried", "Best full test", "Wrong-answer bank"].map((h) => el("th", { scope: "col" }, h)))),
    el("tbody", {}, ...Object.keys(SECTIONS).map(row)));
}

function confirmReset() {
  showModal({
    title: "Reset all progress?",
    body: "This deletes every saved score and empties your wrong-answer bank. It can't be undone.",
    confirmText: "Reset progress",
    cancelText: "Cancel",
    onConfirm: () => {
      resetProgress();
      showHome();
    },
  });
}

// ---------- section page ----------

function showSection(key) {
  const section = SECTIONS[key];
  const mixed = statsFor(`MIX-${key}`);
  const bank = bankIds(key).length;
  clear(app);
  app.append(
    el("a", { class: "back", href: "#/" }, "← Home"),
    el("h1", {}, section.name),
    el("p", { class: "muted" }, sectionDetails(section) + " in exam mode."),
    // (app.append would print "undefined"/"false" for a missing element, so only add it when needed)
    ...(section.generated ? [el("p", { class: "flag generated-note" },
      "These questions were generated for practice. They follow the style of the real test but haven't been " +
      "checked against an official source, so treat an answer you disagree with as a possible error." +
      (section.importedTests ? ` ${importedNote(section.importedTests)}` : ""))] : []),
    el("ul", { class: "test-list" }, ...section.tests.map((n) => testRow(key, n))),
    el("h2", {}, "More practice"),
    el("ul", { class: "test-list" },
      el("li", { class: "test-row" },
        el("div", {},
          el("strong", {}, "Mixed random set"),
          el("p", { class: "muted" },
            `${section.questions} random questions from all ${section.tests.length} tests · ${section.minutes} minutes. ` +
            (mixed.attempts ? `${mixed.attempts} attempt${mixed.attempts > 1 ? "s" : ""} · best ${mixed.best}%` : "Not attempted yet"))),
        el("div", { class: "actions" },
          el("a", { class: "btn primary", href: `#/mixed/${key}/exam` }, "Exam"),
          el("a", { class: "btn", href: `#/mixed/${key}/practice` }, "Practice"))),
      el("li", { class: "test-row" },
        el("div", {},
          el("strong", {}, "Redo wrong answers"),
          el("p", { class: "muted" }, bank
            ? `${bank} question${bank > 1 ? "s" : ""} in your bank. Practice mode; a question leaves the bank after 2 correct answers in a row.`
            : "Your bank is empty. Questions you get wrong will appear here.")),
        el("div", { class: "actions" },
          bank
            ? el("a", { class: "btn primary", href: `#/redo/${key}` }, "Start redo")
            : el("button", { class: "btn", disabled: true }, "Start redo")))));
}

// "Subtest 5 is imported …" / "Subtests 5, 6, 7 are imported …"
function importedNote(tests) {
  const range = tests.length > 1 ? `Subtests ${tests.join(", ")} are` : `Subtest ${tests[0]} is`;
  return `${range} imported from outside question sets and use those sets' answer keys.`;
}

function testRow(key, n) {
  const section = SECTIONS[key];
  const id = testId(key, n);
  const name = section.testNames?.[n];
  const label = name ? `Subtest ${n}: ${name}` : `Test ${n}`;
  const minutes = section.testMinutes?.[n] ?? section.minutes;
  const stats = statsFor(id);
  const summary = stats.attempts
    ? `${stats.attempts} attempt${stats.attempts > 1 ? "s" : ""} · best ${stats.best}% · last ${stats.last}%`
    : "Not attempted yet";
  const imported = section.importedTests?.includes(n);
  return el("li", { class: "test-row" },
    el("div", {},
      el("strong", {}, label),
      imported && el("span", { class: "chip imported" }, "Imported, key from source"),
      el("p", { class: "muted" }, `${minutes} min · ${summary}`)),
    el("div", { class: "actions" },
      el("a", { class: "btn primary", href: `#/quiz/${id}/exam` }, "Exam"),
      el("a", { class: "btn", href: `#/quiz/${id}/practice` }, "Practice")));
}

// ---------- redo, results, errors ----------

async function openRedo(section) {
  const set = await redoSet(section, loadProgress().wrongBank);
  if (!set.questions.length) {
    clear(app);
    app.append(
      el("a", { class: "back", href: `#/section/${section}` }, "← Back to tests"),
      el("h1", {}, "Nothing to redo"),
      el("p", {}, "Your wrong-answer bank for this section is empty."));
    return;
  }
  run(set, "practice");
}

async function openResults(attemptId) {
  const attempt = getAttempt(attemptId);
  if (!attempt) {
    clear(app);
    app.append(
      el("a", { class: "back", href: "#/" }, "← Home"),
      el("h1", {}, "Result not found"),
      el("p", {}, "That result isn't available. It may have been cleared from this browser."));
    return;
  }
  await loadTests([...new Set(attempt.results.map((r) => r.id.split("-")[0]))]);
  showResults(app, attempt);
}

function showError(err) {
  clear(app);
  const fromFile = location.protocol === "file:";
  app.append(el("div", { class: "error" },
    el("h1", {}, "Something went wrong"),
    el("p", {}, err.message),
    fromFile && el("p", {},
      "The page was opened straight from a file, which stops the browser loading the questions. " +
      "Start it with start.bat (or run  python -m http.server 8000  in the site folder) and open http://localhost:8000."),
    el("a", { class: "btn", href: "#/" }, "Home")));
}
