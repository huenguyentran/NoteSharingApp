document.addEventListener("DOMContentLoaded", function () {
    const workspaceGrid = document.querySelector(".workspace-card-grid");
    const loadingMessage = document.getElementById("workspace-loading-message");
    const apiUrlElement = document.getElementById("workspace-api-url");
    const apiUrl = apiUrlElement ? apiUrlElement.dataset.url : '/workspaces/?format=json';

    if (!workspaceGrid) {
        console.error("Không tìm thấy phần tử .workspace-card-grid.");
        return;
    }

    // Hàm để tạo một thẻ workspace
function createWorkspaceCard(workspace) {
    return `
        <div class="workspace-card" data-workspace-id="${workspace.pk}">
            <a href="${workspace.view_url}" class="workspace-card-link">
                <h3 class="workspace-card-title">${workspace.name}</h3>
                <p class="workspace-card-description">${workspace.description ? workspace.description.substring(0, 100) + (workspace.description.length > 100 ? '...' : '') : 'No description provided.'}</p>
                <div class="workspace-card-meta">
                    <span>Created by: ${workspace.owner_username}</span>
                    <span>Created at: ${new Date(workspace.created_at).toLocaleDateString()} ${new Date(workspace.created_at).toLocaleTimeString()}</span>
                    <span>Last updated: ${new Date(workspace.updated_at).toLocaleDateString()} ${new Date(workspace.updated_at).toLocaleTimeString()}</span>
                </div>
            </a>
            <div class="workspace-card-actions">
                <a href="${workspace.edit_url}" class="btn btn-sm btn-info">
                    <i class="fas fa-edit"></i> Edit
                </a>
                <form class="delete-workspace-form d-inline" data-delete-url="${workspace.delete_url}">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
                    <button type="submit" class="btn btn-sm btn-danger">
                        <i class="fas fa-trash-alt"></i> Delete
                    </button>
                </form>
            </div>
        </div>
    `;
}

    // Hàm để lấy CSRF token từ cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Hàm tải và hiển thị workspaces
    function loadWorkspaces(url) {
        if (loadingMessage) {
            loadingMessage.style.display = 'block';
            workspaceGrid.innerHTML = '';
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => {
                        throw new Error(`HTTP error! Status: ${response.status} - ${text}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                if (loadingMessage) {
                    loadingMessage.style.display = 'none';
                }

                if (data.workspaces && data.workspaces.length > 0) {
                    let workspacesHtml = '';
                    data.workspaces.forEach(workspace => {
                        workspacesHtml += createWorkspaceCard(workspace);
                    });
                    workspaceGrid.innerHTML = workspacesHtml;
                    // Gắn event listeners cho các nút delete sau khi các thẻ đã được thêm vào DOM
                    addDeleteEventListeners(); 
                } else {
                    const noWorkspacesMessage = `
                        <p class="no-workspaces-message">
                            ${data.page_info && data.page_info.search_query ? 
                                `No workspaces found matching "${data.page_info.search_query}".` : 
                                `<a href="/workspaces/create/">You don't have any workspaces yet. Start by creating a new one!</a>`}
                        </p>
                    `;
                    workspaceGrid.innerHTML = noWorkspacesMessage;
                }
            })
            .catch(error => {
                console.error("Lỗi khi tải workspace:", error);
                if (loadingMessage) {
                    loadingMessage.style.display = 'none';
                }
                workspaceGrid.innerHTML = "<p class='text-danger'>Không thể tải danh sách workspace. Vui lòng thử lại sau.</p>";
            });
    }

    // HÀM MỚI ĐỂ THÊM LISTENER CHO CÁC FORM DELETE
    function addDeleteEventListeners() {
        document.querySelectorAll('.delete-workspace-form').forEach(form => {
            // Đảm bảo event listener chỉ được thêm một lần
            if (form.dataset.listenerAdded) {
                return;
            }
            form.dataset.listenerAdded = 'true'; // Đánh dấu đã thêm listener

            form.addEventListener('submit', function(e) {
                e.preventDefault(); // Ngăn chặn submit form mặc định

                const confirmDelete = confirm('Are you sure you want to delete this workspace?');
                if (!confirmDelete) {
                    return; // Người dùng hủy xóa
                }

                const deleteUrl = this.dataset.deleteUrl;
                const csrfToken = this.querySelector('input[name="csrfmiddlewaretoken"]').value;
                const workspaceCard = this.closest('.workspace-card'); // Tìm thẻ cha để xóa

                fetch(deleteUrl, {
                    method: 'POST', // Django DeleteWorkspaceView đang mong đợi POST
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json', // Quan trọng
                        'X-Requested-With': 'XMLHttpRequest' // Cho Django biết đây là AJAX
                    },
                    // Không cần body nếu không có dữ liệu thêm để gửi
                    body: JSON.stringify({}) // Gửi một JSON rỗng nếu cần Content-Type application/json
                })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(errorData => {
                            throw new Error(errorData.message || 'Có lỗi khi xóa workspace.');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'success') {
                        if (workspaceCard) {
                            workspaceCard.remove(); // Xóa thẻ workspace khỏi DOM
                        }
                        alert(data.message); // Thông báo thành công
                        // Tùy chọn: Tải lại danh sách workspaces để đảm bảo đồng bộ hoàn toàn
                        // loadWorkspaces(apiUrl); 
                    } else {
                        alert('Lỗi: ' + (data.message || 'Không thể xóa workspace.'));
                    }
                })
                .catch(error => {
                    console.error('Error deleting workspace:', error);
                    alert('Đã xảy ra lỗi không mong muốn: ' + error.message);
                });
            });
        });
    }

    // Gọi hàm tải workspace khi DOM đã sẵn sàng
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('q');
    let initialUrl = apiUrl;
    if (searchQuery) {
        initialUrl += `&q=${encodeURIComponent(searchQuery)}`;
    }
    loadWorkspaces(initialUrl);

    // Xử lý form tìm kiếm (nếu có)
    const searchForm = document.querySelector('.search-section form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchInput = this.querySelector('input[name="q"]');
            const currentSearchQuery = searchInput.value;
            let searchUrl = `${apiUrl}`;
            if (currentSearchQuery) {
                searchUrl += `&q=${encodeURIComponent(currentSearchQuery)}`;
            }
            loadWorkspaces(searchUrl);
            window.history.pushState({ path: searchUrl.replace('?format=json', '') }, '', searchUrl.replace('?format=json', ''));
        });
    }
});