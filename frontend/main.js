document.addEventListener('DOMContentLoaded', function() {
  const chatMessages = document.getElementById("chatMessages");
  const userInput = document.getElementById("userInput");
  const DBSelector = document.getElementById("DBSelector");
  const LLMSelector = document.getElementById("LLMSelector");
  const sendButton = document.getElementById('sendButton');
  const sql_required = document.getElementById('sqlSwitcher');

  if (!sessionStorage.getItem("session_id")) {
    const sessionId = crypto.randomUUID();
    sessionStorage.setItem("session_id", sessionId);
  }
  const session_id = sessionStorage.getItem("session_id");

  // console.log("session_id", session_id);


  function sendMessage() {
    if (!userInput.value.trim()) return;
    if (DBSelector.value === "") {
      alert("Пожалуйста, выберите тип базы данных!");
      return;
    }

    if (LLMSelector.value === "") {
      alert("Пожалуйста, выберите тип LLM!");
      return;
    }

    const userMsg = document.createElement("div");
    userMsg.className = "message user-message";
    userMsg.innerHTML = userInput.value;
    chatMessages.append(userMsg)

    const thinkingMsg = document.createElement("div");
    thinkingMsg.className = "message bot-message";
    thinkingMsg.innerHTML = "⏳ Думаю...";
    chatMessages.append(thinkingMsg);

    fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Session-ID": session_id
      },
      body: JSON.stringify({
        question: userInput.value,
        db_type: DBSelector.value,
        llm_type: LLMSelector.value,
        sql_required: sql_required.checked,
      })
    })
    .then(function(response) {
      if (!response.ok) {
        return response.json().then(err => Promise.reject(err));
      }
      return response.json();
    })
    .then(data => {
      thinkingMsg.remove();
      let formatted_text;
      const explanation = data.explanation.replace(/\n/g, "<br>");
      console.log(sql_required.checked);

      if (sql_required.checked) {
        let result = data.result;
        if (Array.isArray(result)) {
          result = result.map(el => el.join(" | ")).join("<br>");
        }
        formatted_text = `
        <div>🧠 Объяснение:<br>${explanation}</div><br>
        <div>💡 SQL-запрос:</div>
        <pre><code class="language-sql">${data.sql_query}</code></pre><br>
        <div>📊 Результат:<br>${result}</div>
        `;
      }
      else {
        formatted_text = explanation;
      }

      typeBotResponse(formatted_text);
    })
    .catch(error => {
      thinkingMsg.remove();
      const errorMessage = error.detail
        || error.message
        || 'Неизвестная ошибка';
      typeBotResponse(`Произошла ошибка: ${errorMessage}`);
    })

    userInput.value = "";
  }

  function typeBotResponse(text) {
    const botMsg = document.createElement("div");
    botMsg.className = "message bot-message";
    botMsg.innerHTML = text;
    chatMessages.append(botMsg);
  }

  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

});
