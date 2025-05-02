function sendMessage() {
  const chatMessages = document.getElementById("chatMessages");
  const userInput = document.getElementById("userInput");

  if (!userInput.value.trim()) return;

  const userMsg = document.createElement("div");
  userMsg.className = "message user-message";
  userMsg.innerHTML = userInput.value;
  chatMessages.append(userMsg)

  const thinkingMsg = document.createElement("div");
  thinkingMsg.className = "message bot-message";
  thinkingMsg.innerHTML = "⏳ Думаю...";

  setTimeout(function() {
    chatMessages.append(thinkingMsg);
  }, 1200)

  setTimeout(function() {
    fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question: userInput.value})
    })
    .then(function(response) {return response.json();})
    .then(data => {
      thinkingMsg.remove();

    const formatted_text = `
      <div>🧠 Объяснение:<br>${data.explanation}</div><br>
      <div>💡 SQL-запрос:</div>
      <pre><code class="language-sql">${data.sql_query}</code></pre><br>
      <div>📊 Результат:<br>${data.result.map(el => el.join(" | ")).join("<br>")}</div>
    `;

    typeBotResponse(formatted_text);
    })
    .catch(error => {
      thinkingMsg.remove();
      typeBotResponse("Произошла ошибка: ", error.detail)
    })
    userInput.value = "";
  }, 2000)

}

function typeBotResponse(text) {
  const botMsg = document.createElement("div");
  botMsg.className = "message bot-message";
  botMsg.innerHTML = text;
  chatMessages.append(botMsg);
}
