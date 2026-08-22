const button = document.getElementById("listen-button");
const label = button.querySelector(".label");
const hint = document.querySelector(".hint");

const modalOverlay = document.getElementById("modal-overlay");
const modalEyebrow = document.getElementById("modal-eyebrow");
const modalTitle = document.getElementById("modal-title");
const modalClose = document.getElementById("modal-close");

let isListening = false;

button.addEventListener("click", () => {
  if (isListening) return;
  startListening();
});

function startListening() {
  isListening = true;
  button.classList.add("listening");
  label.textContent = "Listening";
  hint.textContent = "Give it a few seconds...";

  fetch("/api/identify", { method: "POST" })
    .then(response => response.json())
    .then(data => showResult(data.title))
    .catch(() => showResult(null));
}

function showResult(title, failureMessage) {
  isListening = false;
  button.classList.remove("listening");
  label.textContent = "Listen";
  hint.textContent = "Hold it up to some music";
  openModal(title, failureMessage);
}

// filenames use underscores instead of spaces, so clean that up for display
function formatTitle(rawTitle) {
  return rawTitle.replace(/_/g, " ");
}

function openModal(title, failureMessage) {
  if (title) {
    modalEyebrow.textContent = "Found it";
    modalTitle.textContent = formatTitle(title);
    modalClose.textContent = "Nice, try another";
  } else {
    modalEyebrow.textContent = "No luck";
    modalTitle.textContent = failureMessage || "Couldn't catch that";
    modalClose.textContent = "Try again";
  }

  modalOverlay.hidden = false;
  requestAnimationFrame(() => modalOverlay.classList.add("open"));
  modalClose.focus();
}

function closeModal() {
  modalOverlay.classList.remove("open");
  setTimeout(() => {
    modalOverlay.hidden = true;
  }, 250);
  button.focus();
}

modalClose.addEventListener("click", closeModal);

modalOverlay.addEventListener("click", (event) => {
  if (event.target === modalOverlay) closeModal();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !modalOverlay.hidden) closeModal();
});
