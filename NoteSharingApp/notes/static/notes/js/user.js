function searchUsers() {
  const keyword = document.getElementById("search-user").value.toLowerCase();
  const users = document.querySelectorAll("#user-list .user-item");

  users.forEach(user => {
    const name = user.getAttribute("data-name");
    user.style.display = name.includes(keyword) ? "block" : "none";
  });
  updateSelectedList();
}

function updateSelectedList() {
  const checkedBoxes = document.querySelectorAll('input[name="share_with_ids"]:checked');
  const selectedList = document.getElementById("selected-user-list");
  selectedList.innerHTML = "";

  checkedBoxes.forEach(box => {
    const label = box.parentElement;
    const name = label.textContent.trim();
    const li = document.createElement("li");
    li.textContent = name;
    selectedList.appendChild(li);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('input[name="share_with_ids"]').forEach(input => {
    input.addEventListener("change", updateSelectedList);
  });
  updateSelectedList();
});
