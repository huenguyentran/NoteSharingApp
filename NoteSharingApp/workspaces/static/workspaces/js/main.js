document.addEventListener("DOMContentLoaded", function () {
    const workspaceGrid = document.querySelector(".workspace-card-grid");
    const loadingMessage = document.getElementById("workspace-loading-message");
    const apiUrlElement = document.getElementById("workspace-api-url");
    const apiUrl = apiUrlElement ? apiUrlElement.dataset.url : '/workspaces/?format=json';

    if (!workspaceGrid) {
        console.error("Không tìm thấy phần tử .workspace-card-grid.");
        return;
    }

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

    function addDeleteEventListeners() {
        document.querySelectorAll('.delete-workspace-form').forEach(form => {
            if (form.dataset.listenerAdded) {
                return;
            }
            form.dataset.listenerAdded = 'true'; 

            form.addEventListener('submit', function(e) {
                e.preventDefault(); 

                const confirmDelete = confirm('Are you sure you want to delete this workspace?');
                if (!confirmDelete) {
                    return;
                }

                const deleteUrl = this.dataset.deleteUrl;
                const csrfToken = this.querySelector('input[name="csrfmiddlewaretoken"]').value;
                const workspaceCard = this.closest('.workspace-card'); 

                fetch(deleteUrl, {
                    method: 'POST', 
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json', 
                        'X-Requested-With': 'XMLHttpRequest' 
                    },
                    body: JSON.stringify({})
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
                            workspaceCard.remove();
                        }
                        alert(data.message); // Thông báo thành công

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

    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('q');
    let initialUrl = apiUrl;
    if (searchQuery) {
        initialUrl += `&q=${encodeURIComponent(searchQuery)}`;
    }
    loadWorkspaces(initialUrl);

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