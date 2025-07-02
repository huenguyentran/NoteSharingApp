document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('#user-list input[name="share_with_ids"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            updateSelectedUsers();
            updateSelectedList();
        });
    });

    updateSelectedList();

    const noSharedUsersMessage = document.getElementById('noSharedUsersMessage');
    const updateShareForm = document.getElementById('updateShareForm');
    if (updateShareForm && updateShareForm.querySelectorAll('.shared-user-item').length > 0) {
        if (noSharedUsersMessage) noSharedUsersMessage.style.display = 'none';
    } else {
        if (noSharedUsersMessage) noSharedUsersMessage.style.display = 'block';
    }

    const selects = document.querySelectorAll('.auto-submit-select');
    selects.forEach(select => {
        select.addEventListener('change', () => {
            const form = document.getElementById('updateShareForm');

            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'update_permissions';
            hiddenInput.value = '1';
            form.appendChild(hiddenInput);

            form.submit();
        });
    });
    
});

async function searchUsers() {
    const keyword = document.getElementById("search-user").value.trim().toLowerCase();
    const userList = document.getElementById("user-list");
    const selectedList = document.getElementById("selected-user-list");

    userList.innerHTML = "<p>Đang tìm kiếm...</p>";
    selectedList.innerHTML = "";

    if (keyword.length < 1) {
        return;
    }
    if (!keyword) {
        userList.innerHTML = "<p>Nhập tên hoặc email để tìm kiếm người dùng.</p>";
        return;
    }

    try {
        const response = await fetch(`/users/?name=${encodeURIComponent(keyword)}`);
        if (!response.ok) throw new Error("Lỗi khi gọi API");

        const users = await response.json();

        if (users.length === 0) {
            userList.innerHTML = "<p>Không tìm thấy người dùng nào.</p>";
            return;
        }

        userList.innerHTML = ""; // clear trước khi render

        users.forEach(user => {
            const label = document.createElement("label");
            label.className = "user-item";
            label.setAttribute("data-id", user.id);
            label.setAttribute("data-name", `${user.username.toLowerCase()} ${user.email.toLowerCase()}`);

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.name = "share_with_ids";
            checkbox.value = user.id;
            checkbox.addEventListener("change", updateSelectedList);

            label.appendChild(checkbox);
            label.append(` ${user.username} (${user.email})`);
            userList.appendChild(label);
        });

    } catch (error) {
        console.error("Lỗi khi tìm kiếm người dùng:", error);
        userList.innerHTML = "<p>Đã xảy ra lỗi khi tìm kiếm.</p>";
    }
}

function updateSelectedList() {
    const checkedBoxes = document.querySelectorAll('input[name="share_with_ids"]:checked');
    const selectedList = document.getElementById("selected-user-list");
    const selectedUsersSection = document.getElementById("selected-users");

    selectedList.innerHTML = "";

    if (checkedBoxes.length > 0) {
        selectedUsersSection.style.display = 'block';
        checkedBoxes.forEach(box => {
            const label = box.parentElement;
            const name = label.textContent.trim();
            const li = document.createElement("li");
            li.textContent = name;
            selectedList.appendChild(li);
        });
    } else {
        selectedUsersSection.style.display = 'none';
    }
}

