// Small DOM helpers used by every screen.

// el("button", { class: "btn", onclick: fn }, "Label") -> <button class="btn">Label</button>
// Props starting with "on" become event listeners; false/null props and children are skipped.
export function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (value == null || value === false) continue;
    if (key === "class") node.className = value;
    else if (key.startsWith("on") && typeof value === "function") node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value === true ? "" : value);
  }
  for (const child of children.flat()) {
    if (child == null || child === false) continue;
    node.append(child instanceof Node ? child : String(child));
  }
  return node;
}

export function clear(node) {
  node.replaceChildren();
}

// In-page confirm dialog (browser confirm() boxes block the page, so we avoid them).
export function showModal({ title, body, confirmText = "OK", cancelText = "Cancel", onConfirm }) {
  const close = () => overlay.remove();
  const confirmButton = el("button", { class: "btn primary", onclick: () => { close(); onConfirm?.(); } }, confirmText);
  const overlay = el("div", { class: "modal-overlay", onclick: (e) => { if (e.target === overlay) close(); } },
    el("div", { class: "modal", role: "dialog", "aria-modal": "true", "aria-labelledby": "modal-title" },
      el("h2", { id: "modal-title" }, title),
      typeof body === "string" ? el("p", {}, body) : body,
      el("div", { class: "modal-actions" },
        cancelText && el("button", { class: "btn", onclick: close }, cancelText),
        confirmButton)));
  overlay.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });
  document.body.append(overlay);
  confirmButton.focus();
}

export function closeModals() {
  document.querySelectorAll(".modal-overlay").forEach((m) => m.remove());
}

// 75 -> "1:15"
export function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

// 54442 -> "54,442"; strings (like "2.1:1") are shown as they are.
export function fmt(value) {
  return typeof value === "number" ? value.toLocaleString("en-GB", { maximumFractionDigits: 3 }) : String(value);
}
