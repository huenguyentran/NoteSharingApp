document.addEventListener("DOMContentLoaded", function () {
    const workspaceGrid = document.querySelector(".workspace-card-grid");
    const loadingMessage = document.getElementById("workspace-loading-message");
    // Lấy URL từ data-url của một phần tử nào đó trong HTML,
    // hoặc bạn có thể nhúng trực tiếp URL từ Django vào script nếu cần.
    // Giả sử bạn sẽ có một div với data-url trên trang Workspace_List.html
    const apiUrlElement = document.getElementById("workspace-api-url");
    const apiUrl = apiUrlElement ? apiUrlElement.dataset.url : '/workspaces/?format=json'; // Fallback nếu không tìm thấy element

    if (!workspaceGrid) {
        console.error("Không tìm thấy phần tử .workspace-card-grid.");
        return;
    }

    // Hàm để tạo một thẻ workspace
    function createWorkspaceCard(workspace) {
        return `
            <div class="workspace-card">
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
                    <form action="${workspace.delete_url}" method="post" class="d-inline" onsubmit="return confirm('Are you sure you want to delete this workspace?');">
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
                // Does this cookie string begin with the name we want?
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
            loadingMessage.style.display = 'block'; // Hiển thị thông báo loading
            workspaceGrid.innerHTML = ''; // Xóa nội dung cũ nếu có
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    // Nếu phản hồi không OK, cố gắng đọc text để xem có lỗi gì từ server không
                    return response.text().then(text => {
                        throw new Error(`HTTP error! Status: ${response.status} - ${text}`);
                    });
                }
                return response.json(); // Bây giờ chúng ta mong đợi JSON
            })
            .then(data => {
                if (loadingMessage) {
                    loadingMessage.style.display = 'none'; // Ẩn thông báo loading
                }

                if (data.workspaces && data.workspaces.length > 0) {
                    let workspacesHtml = '';
                    data.workspaces.forEach(workspace => {
                        workspacesHtml += createWorkspaceCard(workspace);
                    });
                    workspaceGrid.innerHTML = workspacesHtml;
                } else {
                    // Hiển thị thông báo không có workspace
                    const noWorkspacesMessage = `
                        <p class="no-workspaces-message">
                            ${data.page_info && data.page_info.search_query ? 
                                `No workspaces found matching "${data.page_info.search_query}".` : 
                                `<a href="/workspaces/create/">You don't have any workspaces yet. Start by creating a new one!</a>`}
                        </p>
                    `;
                    workspaceGrid.innerHTML = noWorkspacesMessage;
                }
                // TODO: Xử lý hiển thị phân trang ở đây nếu bạn muốn JS quản lý phân trang
                // console.log("Thông tin phân trang:", data.page_info);
            })
            .catch(error => {
                console.error("Lỗi khi tải workspace:", error);
                if (loadingMessage) {
                    loadingMessage.style.display = 'none'; // Ẩn thông báo loading
                }
                workspaceGrid.innerHTML = "<p class='text-danger'>Không thể tải danh sách workspace. Vui lòng thử lại sau.</p>";
            });
    }

    // Gọi hàm tải workspace khi DOM đã sẵn sàng
    // Thêm tham số search_query nếu có từ URL
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
            e.preventDefault(); // Ngăn chặn form submit theo cách truyền thống
            const searchInput = this.querySelector('input[name="q"]');
            const currentSearchQuery = searchInput.value;
            let searchUrl = `${apiUrl}`;
            if (currentSearchQuery) {
                searchUrl += `&q=${encodeURIComponent(currentSearchQuery)}`;
            }
            loadWorkspaces(searchUrl);
            // Cập nhật URL trình duyệt để người dùng có thể chia sẻ hoặc refresh
            window.history.pushState({ path: searchUrl.replace('?format=json', '') }, '', searchUrl.replace('?format=json', ''));
        });
    }
});