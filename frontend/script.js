const button = document.getElementById("listen-button");
const label = button.querySelector(".label");
const hint = document.querySelector(".hint");

const modalOverlay = document.getElementById("modal-overlay");
const modalEyebrow = document.getElementById("modal-eyebrow");
const modalTitle = document.getElementById("modal-title");
const modalClose = document.getElementById("modal-close");

let isListening = false;

const CHUNK_MS = 3000;
const MAX_ATTEMPTS = 15;

button.addEventListener("click", () => {
  if (isListening) return;
  startListening();
});

// records for `durationMs` off an already-open microphone stream and
// resolves with whatever audio it captured
function recordChunk(stream, durationMs) {
  return new Promise((resolve) => {
    const pieces = [];
    const recorder = new MediaRecorder(stream);
    recorder.addEventListener("dataavailable", (event) => pieces.push(event.data));
    recorder.addEventListener("stop", () => resolve(new Blob(pieces, { type: recorder.mimeType })));
    recorder.start();
    setTimeout(() => recorder.stop(), durationMs);
  });
}

function uploadChunk(blob) {
  const formData = new FormData();
  formData.append("audio", blob, "chunk");
  return fetch("/api/identify-chunk", { method: "POST", body: formData })
    .then(response => response.json());
}

async function startListening() {
  isListening = true;
  button.classList.add("listening");
  label.textContent = "Listening";
  hint.textContent = "Give it a few seconds...";

  let stream;
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (error) {
    showResult(null, "Couldn't access your microphone");
    return;
  }

  let title = null;
  let failureMessage = null;

  try {
    await fetch("/api/identify-start", { method: "POST" });

    for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
      const blob = await recordChunk(stream, CHUNK_MS);
      const result = await uploadChunk(blob);
      if (result.found) {
        title = result.title;
        break;
      }
    }
  } catch (error) {
    failureMessage = "Something went wrong, try again";
  }

  stream.getTracks().forEach(track => track.stop());
  showResult(title, failureMessage);
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
