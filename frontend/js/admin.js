// Конфигурация API
//const API_BASE_URL = "http://192.168.99.140:8000";
const API_BASE_URL = "http://localhost:8000";
const USERS_API_URL = `${API_BASE_URL}/api/users`;

const createUserForm = document.getElementById("createUserForm");
const usersList = document.getElementById("usersList");
const refreshBtn = document.getElementById("refreshBtn");
const loadingIndicator = document.getElementById("loadingIndicator");
const messageModal = new bootstrap.Modal(
  document.getElementById("messageModal")
);

// Загрузка пользователей
async function loadUsers() {
  try {
    usersList.innerHTML = "";
    loadingIndicator.style.display = "block";

    const response = await fetch(USERS_API_URL);
    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`);
    }
    const users = await response.json();

    if (users.length === 0) {
      usersList.innerHTML =
        '<div class="col-12 text-center py-4 text-muted">Пользователи не найдены</div>';
      return;
    }

    users.forEach((user) => {
      const userCard = document.createElement("div");
      userCard.className = "col-md-6 col-lg-4 mb-4";
      userCard.innerHTML = `
        <div class="card user-card h-100">
          <div class="card-body">
            <h5 class="card-title">${user.username}</h5>
            <p class="card-text">
              <strong>Email:</strong> ${user.email}<br>
              <strong>Статус:</strong>
              <span class="badge ${user.is_superuser ? 'bg-danger' : 'bg-primary'}">
                ${user.is_superuser ? 'Администратор' : 'Обычный пользователь'}
              </span><br>
              <strong>ID:</strong> ${user.id}
            </p>
          </div>
        </div>
      `;
      usersList.appendChild(userCard);
    });
  } catch (error) {
    showMessage(
      "Ошибка",
      `Не удалось загрузить пользователей: ${error.message}`
    );
  } finally {
    loadingIndicator.style.display = "none";
  }
}

// Создание пользователя
createUserForm.addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
        username,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Неизвестная ошибка");
    }

    const newUser = await response.json();
    showMessage(
      "Успех",
      `Пользователь ${newUser.username} успешно создан!`
    );
    createUserForm.reset();
    loadUsers();
  } catch (error) {
    showMessage(
      "Ошибка",
      `Не удалось создать пользователя: ${error.message}`
    );
  }
});

// Обновление списка пользователей
refreshBtn.addEventListener("click", loadUsers);


function showMessage(title, message) {
  document.getElementById("messageModalTitle").textContent = title;
  document.getElementById("messageModalBody").textContent = message;
  messageModal.show();
}

// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", loadUsers);
