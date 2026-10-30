const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const startButton = document.querySelector("#start");
const stopButton = document.querySelector("#stop");
const sendButton = document.querySelector("#send");
const transcriptBox = document.querySelector("#transcript");
const statusBox = document.querySelector("#status");
const responseBox = document.querySelector("#response");
let recognition;

if (!SpeechRecognition) {
  startButton.disabled = true;
  statusBox.textContent = "Speech recognition is not supported in this browser. Try a browser with Web Speech API support.";
} else {
  recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.onstart = () => {
    startButton.disabled = true;
    stopButton.disabled = false;
    statusBox.textContent = "Listening…";
  };
  recognition.onresult = (event) => {
    let finalText = "";
    let interimText = "";
    for (let i = 0; i < event.results.length; i += 1) {
      const result = event.results[i];
      if (result.isFinal) finalText += result[0].transcript;
      else interimText += result[0].transcript;
    }
    transcriptBox.value = `${finalText}${interimText}`.trim();
  };
  recognition.onerror = (event) => {
    statusBox.textContent = `Recognition error: ${event.error}`;
  };
  recognition.onend = () => {
    startButton.disabled = false;
    stopButton.disabled = true;
    if (statusBox.textContent === "Listening…") statusBox.textContent = "Stopped listening.";
  };
}

startButton.addEventListener("click", () => {
  responseBox.textContent = "";
  recognition.lang = document.querySelector("#language").value;
  try { recognition.start(); } catch (error) { statusBox.textContent = error.message; }
});

stopButton.addEventListener("click", () => recognition.stop());

sendButton.addEventListener("click", async () => {
  const text = transcriptBox.value.trim();
  if (!text) {
    statusBox.textContent = "Record or enter some text first.";
    return;
  }
  sendButton.disabled = true;
  responseBox.textContent = "Sending…";
  try {
    const response = await fetch("/api/transcriptions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
    responseBox.textContent = `Backend response:\n${JSON.stringify(data, null, 2)}`;
    statusBox.textContent = "Transcript sent.";
  } catch (error) {
    responseBox.textContent = `Error: ${error.message}`;
    statusBox.textContent = "Could not send transcript.";
  } finally {
    sendButton.disabled = false;
  }
});
