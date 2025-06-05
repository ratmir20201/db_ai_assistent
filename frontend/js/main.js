document.addEventListener('DOMContentLoaded', async function() {
  const chatMessages = document.getElementById("chatMessages");
  const userInput = document.getElementById("userInput");
  const DBSelector = document.getElementById("DBSelector");
  const LLMSelector = document.getElementById("LLMSelector");
  const sendButton = document.getElementById('sendButton');
  const sql_required = document.getElementById('sqlSwitcher');

  function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
  if (!sessionStorage.getItem("session_id")) {
    const session_id = generateUUID();
    sessionStorage.setItem("session_id", session_id);
  }
  const session_id = sessionStorage.getItem("session_id");


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
    setTimeout(() => {
      thinkingMsg.className = "message bot-message";
      thinkingMsg.innerHTML = "⏳ Думаю...";
      chatMessages.append(thinkingMsg);
    }, 500)


    fetch("http://192.168.99.140:8000/api/chat/messages", {
    // fetch("http://localhost:8000/api/chat/messages", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-Session-ID": session_id,
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
        const messageId = data.message_id
        const explanation = marked.parse(data.explanation);

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
        setTimeout(() => {
          typeBotResponse(formatted_text, messageId);
        }, 550)
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

    function typeBotResponse(text, messageId) {
      const botMsg = document.createElement("div");
      botMsg.className = "message bot-message bot-message-with-review";
      botMsg.innerHTML = `
          ${text}
          <div class="rating-buttons">
              <button class="rate-btn like-btn">
                  <svg viewBox="0 0 24 24" width="20" height="20">
                      <path d="M23,10C23,8.89 22.1,8 21,8H14.68L15.64,3.43C15.66,3.33 15.67,3.22 15.67,3.11C15.67,2.7 15.5,2.32 15.23,2.05L14.17,1L7.59,7.58C7.22,7.95 7,8.45 7,9V19C7,20.1 7.9,21 9,21H18C18.83,21 19.54,20.5 19.84,19.78L22.86,12.73C22.95,12.5 23,12.26 23,12V10M1,21H5V9H1V21Z"/>
                  </svg>
              </button>
              <button class="rate-btn dislike-btn">
                  <svg viewBox="0 0 24 24" width="20" height="20">
                      <path d="M19,15H23V3H19M15,3H6C5.17,3 4.46,3.5 4.16,4.22L1.14,11.27C1.05,11.5 1,11.74 1,12V14C1,15.1 1.9,16 3,16H9.31L8.36,20.57C8.34,20.67 8.33,20.77 8.33,20.88C8.33,21.3 8.5,21.67 8.77,21.94L9.83,23L16.41,16.41C16.78,16.05 17,15.55 17,15V5C17,3.89 16.1,3 15,3Z"/>
                  </svg>
              </button>
          </div>
      `;
      chatMessages.append(botMsg);
      addRatingButtonHandler(botMsg, messageId);
    }

  function addRatingButtonHandler(messageElement, messageId) {
    const likeBtn = messageElement.querySelector(".like-btn")
    const dislikeBtn = messageElement.querySelector(".dislike-btn")
    let isRated = false;
    let currentRating = null;

    async function sendRatingRequest(type) {
      // const url = `http://localhost:8000/api/messages/${messageId}/${type}`;
      const url = `http://192.168.99.140:8000/api/messages/${messageId}/${type}`

      const response = await fetch(url, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "accept": "application/json",
          "X-Session-ID": session_id
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Ошибка запроса");
      }

      return await response.json();
    }


    // async function handleRating(type) {
    //   if (isRated) return;
    //
    //   isRated = true;
    //   likeBtn.disabled = true;
    //   dislikeBtn.disabled = true;
    //
    //   if (type === "like") {
    //     likeBtn.classList.add("active")
    //     dislikeBtn.classList.remove("active");
    //   } else {
    //     dislikeBtn.classList.add("active");
    //     likeBtn.classList.remove("active");
    //   }
    //
    //   // const url = `http://192.168.99.140:8000/api/messages/${messageId}/${type}`
    //   const url = `http://localhost:8000/api/messages/${messageId}/${type}`
    //   await fetch(url, {
    //     method: "POST",
    //     credentials: "include",
    //     headers: {
    //       "Content-Type": "application/json",
    //       "accept": "application/json",
    //       "X-Session-ID": session_id
    //     },
    //   })
    //   .then(function (response) {
    //     if (!response.ok) {
    //       return response.json().then(err => Promise.reject(err));
    //     }
    //     return response.json();
    //   })
    //   .catch(error => {
    //     console.error("Fetch error:", error);
    //     alert(error.detail || "Ошибка запроса");
    //   });
    // }

    function updateButtonStyles() {
      likeBtn.classList.toggle("active", currentRating === "like");
      dislikeBtn.classList.toggle("active", currentRating === "dislike");
    }

    likeBtn.addEventListener("click", async () => {
      if (currentRating === "like") return;

      await sendRatingRequest("like");
      currentRating = "like";
      updateButtonStyles();
    });

    dislikeBtn.addEventListener("click", async () => {
      if (currentRating === "dislike") return;

      await sendRatingRequest("dislike");
      currentRating = "dislike";
      updateButtonStyles();
    });
  }

  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

});
