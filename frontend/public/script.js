const API_URL = "http://127.0.0.1:8000/ask";

const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const spinner = document.getElementById("spinner");

// Send on Enter key
userInput.addEventListener("keydown", function(e) {
  if (e.key === "Enter") {
    handleSend();
  }
});

async function handleSend() {
  const question = userInput.value.trim();
  if (!question) return;

  addUserMessage(question);
  userInput.value = "";
  setLoading(true);

  try {
    console.log("Sending request to:", API_URL);

    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question }),
    });

    console.log("Response status:", response.status);

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();
    console.log("Data received:", data);
    addBotMessage(data.answer, data.sources);

  } catch (err) {
    console.error("Error:", err);
    addBotMessage(
      "⚠️ Error: " + err.message + ". Please make sure the backend is running at http://127.0.0.1:8000",
      []
    );
  } finally {
    setLoading(false);
  }
}

function addUserMessage(text) {
  const msg = document.createElement("div");
  msg.className = "message user";
  msg.innerHTML = `
    <div class="avatar user-avatar">You</div>
    <div class="bubble">${escapeHtml(text)}</div>
  `;
  chatContainer.appendChild(msg);
  scrollToBottom();
}

function addBotMessage(markdownText, sources) {
  const msg = document.createElement("div");
  msg.className = "message bot";

  const renderedAnswer = marked.parse(markdownText);

  let sourcesHtml = "";
  if (sources && sources.length > 0) {
    sourcesHtml = `
      <details class="sources">
        <summary>View source excerpts (${sources.length})</summary>
        ${sources.map((s, i) =>
          `<div class="source-item"><strong>Source ${i + 1}:</strong>\n${escapeHtml(s.content)}</div>`
        ).join("")}
      </details>
    `;
  }

  msg.innerHTML = `
    <div class="avatar bot-avatar">SSC</div>
    <div class="bubble">${renderedAnswer}${sourcesHtml}</div>
  `;

  chatContainer.appendChild(msg);
  scrollToBottom();
}

function setLoading(isLoading) {
  sendBtn.disabled = isLoading;
  spinner.classList.toggle("active", isLoading);
}

function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Topic chips
document.querySelectorAll(".sub-bar span").forEach((chip) => {
  chip.style.cursor = "pointer";
  chip.addEventListener("click", () => {
    const topic = chip.textContent.trim();
    const questions = {
      "📋 Eligibility": "What are the eligibility criteria for SSC CGL 2026?",
      "💰 Fees": "What is the application fee and who is exempted?",
      "📅 Important Dates": "What are the important dates for SSC CGL 2026?",
      "📝 Exam Pattern": "What is the exam pattern for Tier-I and Tier-II?",
      "📄 Documents": "What documents are required for the application?",
    };
    userInput.value = questions[topic] || topic;
    userInput.focus();
  });
});