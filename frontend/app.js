const API_BASE = "http://localhost:8000";

const answer = document.getElementById("answer");
const summary = document.getElementById("summary");

document.getElementById("askBtn").addEventListener("click", async () => {
  answer.textContent = "Analyzing enterprise context...";

  const payload = {
    question: document.getElementById("question").value,
    role: document.getElementById("role").value,
    user_id: "demo-user",
    max_context_events: 5
  };

  try {
    const response = await fetch(`${API_BASE}/ask-ai`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      answer.textContent = JSON.stringify(data, null, 2);
      return;
    }

    answer.textContent =
      `Confidence: ${data.confidence}\n\n` +
      `${data.answer}\n\n` +
      `Retrieved Events:\n${JSON.stringify(data.retrieved_events, null, 2)}`;
  } catch (error) {
    answer.textContent = `Error: ${error.message}`;
  }
});

document.getElementById("summaryBtn").addEventListener("click", async () => {
  summary.textContent = "Loading summary...";

  try {
    const response = await fetch(`${API_BASE}/reports/summary`);
    const data = await response.json();
    summary.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    summary.textContent = `Error: ${error.message}`;
  }
});
