document.getElementById('exitButton').addEventListener('click', async () => {
  const response = await fetch("http://localhost:8000/auth/logout", {
    method: "POST",
    credentials: "include",
  });

  if (response.ok) {
    window.location.href = "/login";
  } else {
    alert("Ошибка при выходе");
  }
});
