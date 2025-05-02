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
      🧠 Объяснение:
      ${data.explanation}

      💡 SQL-запрос:
      \`\`\`sql
      ${data.sql_query}
      \`\`\`

      📊 Результат:
      ${data.result.map(el => el.join(" | ")).join("\n")}
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
    chatMessages.append(botMsg);

    let i = 0;
    const interval = setInterval(function() {
      botMsg.innerHTML += text[i];
      i++;
      if (i >= text.length) {
        clearInterval(interval);
      }
    }, 30)
}
