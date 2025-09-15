// Lấy phần tử DOM
const input = document.getElementById("task-input");
const addBtn = document.getElementById("add-btn");
const taskList = document.getElementById("task-list");

// Hàm thêm công việc
function addTask() {
  const taskText = input.value.trim();
  if (taskText === "") {
    alert("Vui lòng nhập công việc!");
    return;
  }

  // Tạo <li>
  const li = document.createElement("li");
  li.innerText = taskText;

  // Nút Hoàn thành
  const doneBtn = document.createElement("button");
  doneBtn.innerText = "✔";
  doneBtn.style.background = "green";
  doneBtn.addEventListener("click", () => {
    li.classList.toggle("done");
  });

  // Nút Xóa
  const deleteBtn = document.createElement("button");
  deleteBtn.innerText = "🗑";
  deleteBtn.addEventListener("click", () => {
    li.remove();
  });

  // Thêm nút vào li
  li.appendChild(doneBtn);
  li.appendChild(deleteBtn);

  // Thêm li vào danh sách
  taskList.appendChild(li);

  // Xóa input
  input.value = "";
}

// Sự kiện nút thêm
addBtn.addEventListener("click", addTask);

// Sự kiện Enter
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    addTask();
  }
});
