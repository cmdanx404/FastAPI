const API_URL = "http://127.0.0.1:8000/todos/";

async function fetchTodos() {
  try {
    const response = await fetch(API_URL);
    const todos = await response.json();
    renderTodos(todos);
  } catch (error) {
    showNotification("❌ Failed to load todos", "error");
  }
}

function renderTodos(todos) {
  const list = document.getElementById("todo-list");
  list.innerHTML = "";

  if (todos.length === 0) {
    list.innerHTML = "<p style='text-align:center;color:#777'>No todos yet!</p>";
    return;
  }

  todos.forEach(todo => {
    const card = document.createElement("div");
    card.className = "todo-card";

    card.innerHTML = `
      <div class="todo-info">
        <div class="todo-title">${todo.title}</div>
        <div class="todo-desc">${todo.description || ""}</div>
        <span class="status ${todo.completed ? "done" : "pending"}">
          ${todo.completed ? "Done ✅" : "Pending ⏳"}
        </span>
      </div>
      <div class="todo-actions">
        ${!todo.completed ? `<button class="complete-btn" onclick="completeTodo(${todo.id})">Complete</button>` : ""}
        <button class="delete-btn" onclick="deleteTodo(${todo.id})">Delete</button>
      </div>
    `;
    list.appendChild(card);
  });
}

async function addTodo() {
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;

  if (!title.trim()) {
    showNotification("⚠️ Title is required!", "error");
    return;
  }

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, description })
    });

    if (!res.ok) throw new Error();

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";

    showNotification("✅ Todo added successfully!", "success");
    fetchTodos();
  } catch (error) {
    showNotification("❌ Failed to add todo", "error");
  }
}

async function completeTodo(id) {
  try {
    const res = await fetch(API_URL + id, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: true })
    });

    if (!res.ok) throw new Error();

    showNotification("✅ Todo marked as completed", "success");
    fetchTodos();
  } catch {
    showNotification("❌ Failed to complete todo", "error");
  }
}

async function deleteTodo(id) {
  try {
    const res = await fetch(API_URL + id, { method: "DELETE" });
    if (!res.ok) throw new Error();

    showNotification("🗑️ Todo deleted", "success");
    fetchTodos();
  } catch {
    showNotification("❌ Failed to delete todo", "error");
  }
}

function showNotification(message, type) {
  const note = document.getElementById("notification");
  note.textContent = message;
  note.className = type;
  setTimeout(() => {
    note.textContent = "";
    note.className = "";
  }, 2500);
}

// Initial load
fetchTodos();
