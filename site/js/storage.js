// Progress saved in this browser (localStorage).
// Storage can be blocked (private windows, strict settings), so every access is
// wrapped in try/catch and the site keeps working, just without saving.

const KEY = "pwc.progress.v1";
const inMemory = []; // attempts from this visit, in case storage is blocked

function empty() {
  return { attempts: [], wrongBank: {} };
}

export function loadProgress() {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? { ...empty(), ...JSON.parse(raw) } : empty();
  } catch {
    return empty();
  }
}

function save(progress) {
  try {
    localStorage.setItem(KEY, JSON.stringify(progress));
  } catch {
    // storage unavailable or full: nothing else we can do
  }
}

// Wrong-answer bank: a miss adds the question; getting it right twice in a row removes it.
function updateBank(bank, id, isCorrect) {
  if (!isCorrect) {
    const entry = bank[id] ?? { misses: 0, streak: 0 };
    entry.misses += 1;
    entry.streak = 0;
    bank[id] = entry;
  } else if (bank[id]) {
    bank[id].streak += 1;
    if (bank[id].streak >= 2) delete bank[id];
  }
}

export function recordAttempt(attempt) {
  inMemory.push(attempt);
  const progress = loadProgress();
  progress.attempts.push(attempt);
  for (const r of attempt.results) {
    if (r.scored) updateBank(progress.wrongBank, r.id, r.isCorrect);
  }
  save(progress);
}

export function getAttempt(id) {
  return loadProgress().attempts.find((a) => a.id === id) ?? inMemory.find((a) => a.id === id);
}

export function resetProgress() {
  inMemory.length = 0;
  try {
    localStorage.removeItem(KEY);
  } catch {
    // nothing saved, nothing to clear
  }
}

const pct = (a) => (a.total ? Math.round((a.score / a.total) * 100) : 0);

function summarise(attempts) {
  return {
    attempts: attempts.length,
    best: attempts.length ? Math.max(...attempts.map(pct)) : null,
    last: attempts.length ? pct(attempts[attempts.length - 1]) : null,
  };
}

// { attempts: 3, best: 85, last: 70 } (scores in %) for one test, mixed set or redo set.
export function statsFor(setId) {
  return summarise(loadProgress().attempts.filter((a) => a.testId === setId));
}

// Question ids in the wrong-answer bank for one section ("N…" or "V…").
export function bankIds(section) {
  const prefix = section === "numerical" ? "N" : "V";
  return Object.keys(loadProgress().wrongBank).filter((id) => id.startsWith(prefix));
}

// Home-screen summary for a section: attempts, best full-test score, bank size.
export function sectionSummary(section) {
  const prefix = section === "numerical" ? "N" : "V";
  const attempts = loadProgress().attempts.filter((a) => a.testId.startsWith(prefix) || a.section === section);
  const fullTests = attempts.filter((a) => /^[NV]\d+$/.test(a.testId));
  const best = fullTests.length ? fullTests.reduce((x, y) => (pct(y) > pct(x) ? y : x)) : null;
  return {
    attempts: attempts.length,
    testsTried: new Set(fullTests.map((a) => a.testId)).size,
    bestPct: best ? pct(best) : null,
    bestTitle: best?.title ?? null,
    bank: bankIds(section).length,
  };
}
