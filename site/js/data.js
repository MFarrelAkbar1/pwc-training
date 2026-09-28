// Which tests exist, how to load them from site/data/*.json,
// and how to build question sets (single test, mixed random set, wrong-answer redo).

// prefix: first letter of every test and question id in the section ("N3", "N3-Q04").
// minutes / questions: per test, also used for the mixed random set.
// testMinutes / testQuestions / testNames: per-test overrides (Logic subtests have their own timers,
// and the entrance-test papers V8 and N6 are 15 questions in 15 minutes).
// generated: questions were written for this site, not taken from the source PDF.
// importedTests: tests in a generated section that were imported from an outside source instead (key from that source).
// A test's exam timer is testMinutes when set, otherwise the timeLimitSec in its JSON.
// Timer for each of the four subtests imported from the figural question bank (L6–L9, 17 questions each).
const FIGURAL_BANK_MINUTES = 17;

export const SECTIONS = {
  numerical: {
    name: "Numerical Reasoning", short: "Numerical", prefix: "N", tests: [1, 2, 3, 4, 5, 6], minutes: 17, questions: 20,
    testMinutes: { 6: 15 }, testQuestions: { 6: 15 },
  },
  verbal: {
    name: "Verbal Reasoning", short: "Verbal", prefix: "V", tests: [1, 2, 3, 4, 5, 6, 7, 8], minutes: 8, questions: 15,
    testMinutes: { 8: 15 },
  },
  english: { name: "English (TOEFL-style)", short: "English", prefix: "E", tests: [1, 2, 3], minutes: 15, questions: 20, generated: true },
  logic: {
    name: "Logic (TPA-style)", short: "Logic", prefix: "L", tests: [1, 2, 3, 4, 5, 6, 7, 8, 9], minutes: 10, questions: 15,
    generated: true,
    // Subtest 5 timer: 17 minutes for 17 questions. Change it here (its JSON has no timeLimitSec).
    // Subtests 6–9 (figural question bank) all use FIGURAL_BANK_MINUTES above.
    testMinutes: {
      1: 10, 2: 12, 3: 8, 4: 12, 5: 17,
      6: FIGURAL_BANK_MINUTES, 7: FIGURAL_BANK_MINUTES, 8: FIGURAL_BANK_MINUTES, 9: FIGURAL_BANK_MINUTES,
    },
    testQuestions: { 5: 17, 6: 17, 7: 17, 8: 17, 9: 17 },
    testNames: {
      1: "Number sequences", 2: "Figure patterns", 3: "Analogies", 4: "Syllogisms", 5: "Figural patterns (extra hard)",
      6: "Figural analogies", 7: "Odd one out", 8: "Figural series", 9: "Figural matrices",
    },
    importedTests: [5, 6, 7, 8, 9],
  },
  technical: { name: "Technical (Risk Assurance)", short: "Technical", prefix: "T", tests: [1, 2, 3], minutes: 20, questions: 20, generated: true },
};

// "N" -> "numerical", "L" -> "logic", …
const SECTION_BY_PREFIX = Object.fromEntries(Object.entries(SECTIONS).map(([key, s]) => [s.prefix, key]));

export function sectionOfId(id) {
  return SECTION_BY_PREFIX[id[0]];
}

export function isTestId(id) {
  return /^[A-Z]\d+$/.test(id) && SECTIONS[sectionOfId(id)]?.tests.includes(Number(id.slice(1)));
}

export function testId(section, number) {
  return SECTIONS[section].prefix + number;
}

export function allTestIds(section) {
  return SECTIONS[section].tests.map((n) => testId(section, n));
}

// "N3-Q04" -> "N3"; "L2-Q10" -> "logic"
export const testIdOf = (q) => q.id.split("-")[0];
export const sectionOf = (q) => sectionOfId(q.id);

function testFile(id) {
  return `data/${sectionOfId(id)}-${id.slice(1)}.json`;
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

// Every letter that counts as correct. Usually just correctAnswer(q); acceptedAnswers lists more
// when two options are equally right (e.g. the same ratio written two ways).
export function acceptedAnswers(q) {
  const correct = correctAnswer(q);
  if (correct == null) return [];
  return q.acceptedAnswers ?? [correct];
}

export const isAccepted = (q, letter) => letter != null && acceptedAnswers(q).includes(letter);

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
  const section = sectionOfId(id);
  const minutes = SECTIONS[section].testMinutes?.[Number(id.slice(1))];
  const timeLimitSec = minutes ? minutes * 60 : test.timeLimitSec;
  return { kind: "test", id, section, title: test.title, timeLimitSec, questions: test.questions };
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
