async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatLog = document.getElementById("chat-log");
  const message = input.value.trim();

  if (!message) return;

  chatLog.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
  input.value = "";

  try {
    const res = await fetch("http://localhost:8080/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    const reply = data.reply || data.error || "No reply";
    chatLog.innerHTML += `<div><strong>Bot:</strong> ${reply}</div>`;
    chatLog.scrollTop = chatLog.scrollHeight;

  } catch (err) {
    chatLog.innerHTML += `<div><strong>Error:</strong> Could not reach server.</div>`;
  }
}
