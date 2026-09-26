// Which tests exist, how to load them from site/data/*.json,
// and how to build question sets (single test, mixed random set, wrong-answer redo).

export const SECTIONS = {
  numerical: { name: "Numerical Reasoning", tests: [1, 2, 3, 4, 5], minutes: 17, questions: 20 },
  verbal: { name: "Verbal Reasoning", tests: [1, 2, 3, 4, 5, 6, 7], minutes: 8, questions: 15 },
};

export function testId(section, number) {
  return (section === "numerical" ? "N" : "V") + number;
}

export function allTestIds(section) {
  return SECTIONS[section].tests.map((n) => testId(section, n));
}

// "N3-Q04" -> "N3"; "V2-Q10" -> "verbal"
export const testIdOf = (q) => q.id.split("-")[0];
export const sectionOf = (q) => (q.id.startsWith("N") ? "numerical" : "verbal");

function testFile(id) {
  const section = id.startsWith("N") ? "numerical" : "verbal";
  return `data/${section}-${id.slice(1)}.json`;
}

const requests = new Map(); // id -> Promise<test>
const loaded = new Map(); // id -> test, once it has arrived

export function loadTest(id) {
  if (!requests.has(id)) {
    const request = fetch(testFile(id)).then((response) => {
      if (!response.ok) throw new Error(`Could not load ${testFile(id)} (${response.status})`);
      return response.json();
    });
    request.then((test) => loaded.set(id, test), () => requests.delete(id)); // allow a retry after a failure
    requests.set(id, request);
  }
  return requests.get(id);
}

export function loadTests(ids) {
  return Promise.all(ids.map(loadTest));
}

// The test a question belongs to (its test must already be loaded).
export function testOf(q) {
  return loaded.get(testIdOf(q));
}

export function findQuestion(id) {
  return loaded.get(id.split("-")[0])?.questions.find((q) => q.id === id);
}

// The answer the site scores against: our verified answer when the source key
// was corrected, otherwise the PDF key. null means the question isn't scored.
export function correctAnswer(q) {
  return "verifiedAnswer" in q ? q.verifiedAnswer : q.answer;
}

export const isScored = (q) => correctAnswer(q) != null;

export function shuffle(items) {
  const a = [...items];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ---------- question sets ----------
// A "set" is what a quiz runs: { kind, id, section, title, timeLimitSec, questions }.
// Its id is what attempts are saved under ("N1", "MIX-numerical", "REDO-verbal").

export async function singleTestSet(id) {
  const test = await loadTest(id);
  const section = id.startsWith("N") ? "numerical" : "verbal";
  return { kind: "test", id, section, title: test.title, timeLimitSec: test.timeLimitSec, questions: test.questions };
}

// Random questions from every test in the section. Unscored (dropped) questions are never included.
export async function mixedSet(section) {
  const tests = await loadTests(allTestIds(section));
  const pool = tests.flatMap((t) => t.questions).filter(isScored);
  const { questions, minutes, name } = SECTIONS[section];
  return {
    kind: "mixed",
    id: `MIX-${section}`,
    section,
    title: `${name} – Mixed random set`,
    timeLimitSec: minutes * 60,
    questions: shuffle(pool).slice(0, questions),
  };
}

// Every question in the wrong-answer bank for this section, in random order.
export async function redoSet(section, bank) {
  await loadTests(allTestIds(section));
  const questions = Object.keys(bank)
    .map(findQuestion)
    .filter((q) => q && sectionOf(q) === section && isScored(q));
  return {
    kind: "redo",
    id: `REDO-${section}`,
    section,
    title: `${SECTIONS[section].name} – Redo wrong answers`,
    timeLimitSec: SECTIONS[section].minutes * 60,
    questions: shuffle(questions),
  };
}
