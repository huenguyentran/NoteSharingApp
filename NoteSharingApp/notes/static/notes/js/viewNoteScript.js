// Lấy các phần tử HTML
const commentsSection = document.getElementById('comments-section');
const toggleCommentsButton = document.getElementById('toggle-comments');
const commentsList = document.getElementById('comments-list');
const commentContentInput = document.getElementById('comment-content');
const submitCommentButton = document.getElementById('submit-comment');
const commentErrorMessage = document.getElementById('comment-error-message');
const prevPageButton = document.getElementById('prev-page');
const nextPageButton = document.getElementById('next-page');
const currentPageInfo = document.getElementById('current-page-info');

// Biến lưu trữ trạng thái phân trang, lấy NOTE_ID và CSRF_TOKEN từ Django context
const noteMeta = document.getElementById('note-meta');
const NOTE_ID = noteMeta.dataset.noteId;
const CURRENT_USER = noteMeta.dataset.user;
const IS_AUTHENTICATED = noteMeta.dataset.authenticated;
const CSRF_TOKEN = noteMeta.dataset.csrf;

let currentPage = 1;
let totalPages = 1;
let commentsLoaded = false; // Biến mới để theo dõi xem comments đã được tải lần đầu chưa

/**
 * Hàm để lấy CSRF token.
 */
function getCsrfToken() {
    return CSRF_TOKEN;
}

/**
 * Hiển thị thông báo lỗi.
 * @param {string} message - Nội dung thông báo lỗi.
 */
function displayError(message) {
    commentErrorMessage.textContent = message;
    commentErrorMessage.style.display = 'block';
}

/**
 * Xóa thông báo lỗi.
 */
function clearError() {
    commentErrorMessage.textContent = '';
    commentErrorMessage.style.display = 'none';
}

/**
 * Hàm format thời gian hiển thị.
 * @param {string} isoString - Chuỗi thời gian ISO từ server (ví dụ: "2024-07-02T10:30:00Z").
 * @returns {string} Chuỗi thời gian đã format.
 */
function formatDateTime(isoString) {
    const date = new Date(isoString);
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false // 24-hour format
    };
    // Đặt múi giờ nếu server và client khác múi giờ
    // options.timeZone = 'Asia/Ho_Chi_Minh'; // Ví dụ: múi giờ Việt Nam
    return date.toLocaleDateString('vi-VN', options) + ' ' + date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', hour12: false });
}


/**
 * Tải danh sách comments cho note hiện tại.
 * @param {number} page - Số trang comments muốn tải.
 */
async function fetchComments(page) {
    clearError();
    if (!NOTE_ID) {
        console.error("NOTE_ID is not defined. Cannot load comments.");
        displayError("Lỗi: Không thể tải bình luận. ID ghi chú không xác định.");
        return;
    }
    try {
        const response = await fetch(`/comments/note/${NOTE_ID}/?page=${page}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        renderComments(data);
        commentsLoaded = true; // Đánh dấu là comments đã được tải ít nhất một lần
        console.log('Comments data:', data);
    } catch (error) {
        console.error('Error fetching comments:', error);
        displayError('Không thể tải bình luận. Vui lòng thử lại.');
    }
}

/**
 * Render danh sách comments lên giao diện.
 * @param {Object} data - Dữ liệu comments từ API (bao gồm comments, current_page, total_pages...).
 */
function renderComments(data) {
    commentsList.innerHTML = ''; // Xóa comments cũ
    if (data.comments && data.comments.length > 0) {
        data.comments.forEach(comment => {
            const li = document.createElement('li');
            li.className = 'comment-item';
            li.setAttribute('data-comment-id', comment.id); // Lưu ID comment
            li.innerHTML = `
                <div class="comment-header">
                    <span class="comment-user">${comment.user}</span>
                    <span class="comment-meta">${formatDateTime(comment.created_at)}</span>
                </div>
                <div class="comment-content">${comment.content}</div>
                <div class="comment-actions">
                    ${comment.user === CURRENT_USER && IS_AUTHENTICATED === 'true' ? `
                    <button class="delete-button" data-comment-id="${comment.id}"><i class="fas fa-trash-alt"></i> Xóa</button>
                    ` : ''}
                </div>
            `;
            commentsList.appendChild(li);
        });
        attachDeleteEventListeners(); // Gắn lại sự kiện xóa cho các nút mới
    } else {
        commentsList.innerHTML = '<li class="text-center text-muted">Chưa có bình luận nào.</li>';
    }

    // Cập nhật thông tin phân trang
    currentPage = data.current_page;
    totalPages = data.total_pages;
    currentPageInfo.textContent = `Trang ${currentPage} / ${totalPages}`;

    prevPageButton.disabled = !data.has_previous;
    nextPageButton.disabled = !data.has_next;
}

/**
 * Gửi comment mới đến server.
 */
async function postComment() {
    clearError();
    const content = commentContentInput.value.trim();

    if (!content) {
        return;
    }

    try {
        const response = await fetch('/comments/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(), // Sử dụng CSRF token
            },
            body: JSON.stringify({
                note_id: NOTE_ID,
                content: content
            })
        });

        const data = await response.json();

        if (response.ok) {
            commentContentInput.value = ''; // Xóa nội dung input
            // Tải lại trang đầu tiên để thấy comment mới
            currentPage = 1; // Reset về trang 1 sau khi gửi comment
            await fetchComments(currentPage);
            console.log('Comment created:', data);
        } else {
            displayError(data.error || 'Gửi bình luận thất bại. Vui lòng thử lại.');
            console.error('Error creating comment:', data);
        }
    } catch (error) {
        console.error('Error submitting comment:', error);
        displayError('Đã xảy ra lỗi khi gửi bình luận. Vui lòng thử lại.');
    }
}

/**
 * Xóa comment.
 * @param {number} commentId - ID của comment cần xóa.
 */
async function deleteComment(commentId) {
    if (!confirm('Bạn có chắc chắn muốn xóa bình luận này không?')) {
        return;
    }
    clearError();
    try {
        const response = await fetch(`/comments/${commentId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken(), // Sử dụng CSRF token
            },
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Comment deleted:', data.message);
            // Tải lại comments của trang hiện tại sau khi xóa
            await fetchComments(currentPage);
        } else {
            displayError(data.error || 'Xóa bình luận thất bại. Vui lòng thử lại.');
            console.error('Error deleting comment:', data);
        }
    } catch (error) {
        console.error('Error deleting comment:', error);
        displayError('Đã xảy ra lỗi khi xóa bình luận. Vui lòng thử lại.');
    }
}

/**
 * Gắn sự kiện click cho các nút xóa comment.
 */
function attachDeleteEventListeners() {
    document.querySelectorAll('.comment-actions .delete-button').forEach(button => {
        button.onclick = (event) => {
            // Lấy commentId từ dataset của nút hoặc phần tử cha gần nhất
            const commentId = event.target.dataset.commentId || event.target.closest('button').dataset.commentId;
            if (commentId) {
                deleteComment(commentId);
            }
        };
    });
}

// Event Listener cho nút ẩn/hiện bình luận
toggleCommentsButton.addEventListener('click', () => {
    if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
        commentsSection.style.display = 'block';
        toggleCommentsButton.innerHTML = '<i class="fas fa-comments"></i> Ẩn Bình luận';
        // Nếu comments chưa được tải lần nào, thì tải chúng
        if (!commentsLoaded) {
            fetchComments(currentPage);
        }
    } else {
        commentsSection.style.display = 'none';
        toggleCommentsButton.innerHTML = '<i class="fas fa-comments"></i> Xem Bình luận';
    }
});

// Event Listeners cho các nút bình luận (chỉ khi người dùng đã đăng nhập)
if (IS_AUTHENTICATED === 'true') {
    submitCommentButton.addEventListener('click', postComment);
}

prevPageButton.addEventListener('click', () => {
    if (currentPage > 1) {
        fetchComments(currentPage - 1);
    }
});

nextPageButton.addEventListener('click', () => {
    if (currentPage < totalPages) {
        fetchComments(currentPage + 1);
    }
});

// Hàm sao chép link chia sẻ
function copyShareLink() {
    const shareLinkInput = document.getElementById('shareLink');
    shareLinkInput.select();
    shareLinkInput.setSelectionRange(0, 99999); // For mobile devices

    navigator.clipboard.writeText(shareLinkInput.value).then(() => {
        alert('Liên kết đã được sao chép vào bộ nhớ tạm!');
    }).catch(err => {
        console.error('Không thể sao chép liên kết: ', err);
    });
}