// Quiz state and scoring. No DOM code here.
import { correctAnswer } from "./data.js";

// set = { kind, id, section, title, timeLimitSec, questions } (see data.js)
export function createQuiz({ set, mode, timeLimitSec }) {
  const now = Date.now();
  return {
    set,
    mode, // "exam" or "practice"
    questions: set.questions,
    timeLimitSec,
    index: 0,
    answers: {}, // question id -> chosen letter
    marked: new Set(), // question ids marked for review (exam)
    startedAt: now,
    endsAt: mode === "exam" ? now + timeLimitSec * 1000 : null,
    finishedAt: null,
    autoSubmitted: false,
  };
}

// Timing uses the clock, not a counter, so it stays right if the tab is in the background.
export function secondsLeft(quiz) {
  return Math.max(0, Math.ceil((quiz.endsAt - Date.now()) / 1000));
}

export function elapsedSeconds(quiz) {
  return Math.round(((quiz.finishedAt ?? Date.now()) - quiz.startedAt) / 1000);
}

// The record we save and show on the results screen.
export function buildAttempt(quiz) {
  const results = quiz.questions.map((q) => {
    const correct = correctAnswer(q);
    const chosen = quiz.answers[q.id] ?? null;
    return { id: q.id, chosen, correct, scored: correct != null, isCorrect: correct != null && chosen === correct };
  });
  const scored = results.filter((r) => r.scored);
  return {
    id: `${quiz.set.id}-${quiz.startedAt}`,
    testId: quiz.set.id,
    kind: quiz.set.kind,
    section: quiz.set.section,
    title: quiz.set.title,
    mode: quiz.mode,
    date: new Date(quiz.startedAt).toISOString(),
    timeUsedSec: elapsedSeconds(quiz),
    timeLimitSec: quiz.timeLimitSec,
    autoSubmitted: quiz.autoSubmitted,
    score: scored.filter((r) => r.isCorrect).length,
    total: scored.length,
    results,
  };
}
