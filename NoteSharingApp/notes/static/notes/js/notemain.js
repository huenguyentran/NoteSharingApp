
// Cần: filter (của tôi theo title....) (API ở Note) 
//+ Btn load more(hoặc là gì đó giống)_vì đang dùng phân trang
//+ Tạo mới ghi chú -> direct sang trang tạo ghi chú
//+ Xem ghi chú (trong trang xem ghi chú: chỉnh sửa (nếu đc) + set quyền truy cập + xem comment của ghi chú)





// Gọi hàm fetch khi trang load
window.addEventListener('DOMContentLoaded', async () => {
    const data = await fetchNotes();
    if (data && data.notes) {
        renderNotes(data.notes);
    }
});

async function fetchNotes({
    search = '',
    permission = '',
    createdByMe = false,
    page = 1
} = {}) {
    const params = new URLSearchParams();

    if (search) params.append('search', search);
    if (permission) params.append('permission', permission);
    if (createdByMe) params.append('created_by_me', 'true');
    if (page) params.append('page', page);

    try {
        const response = await fetch(`/notes/?${params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                // 'X-CSRFToken': getCookie('csrftoken'), // nếu cần
            },
            credentials: 'include'  // gửi cookie để xác thực user login
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Notes:', data);
        return data;

    } catch (error) {
        console.error('Error fetching notes:', error);
    }
}

function renderNotes(notes) {
    const listEl = document.getElementById('note-list');
    listEl.innerHTML = ''; // Xóa danh sách cũ

    if (notes.length === 0) {
        listEl.innerHTML = '<li class="no-notes"><p>You don\'t have any notes yet. Start by adding a new one!</p></li>';
        return;
    }

    notes.forEach(note => {
        const li = document.createElement('li');
        li.className = 'note-item';
        li.innerHTML = `
            <strong>${note.title}</strong>
            <div class="note-content">${note.content}</div>
            <div class="note-meta">
                <span>Permission: ${note.permission}</span>
                <span>Updated at: ${note.updated_at}</span>
            </div>
        `;
        listEl.appendChild(li);
    });
}
