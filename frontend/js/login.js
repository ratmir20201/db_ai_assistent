// Конфигурация API
//const API_BASE_URL = "http://192.168.99.140:8000";
const API_BASE_URL = "http://localhost:8000";


document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;
    const email = form.username.value;
    const password = form.password.value;

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ username: email, password }),
    });

    if (response.ok) {
      window.location.href = "/";
    } else {
      alert("Ошибка входа");
    }
  });
