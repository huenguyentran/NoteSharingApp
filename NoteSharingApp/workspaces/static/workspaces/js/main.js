document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("workspace-container");
  const url = container.dataset.url; // Lấy từ data-url

  fetch(url)
    .then(response => {
      if (!response.ok) throw new Error("Lỗi mạng");
      return response.text();
    })
    .then(html => {
      container.innerHTML = html;
    })
    .catch(error => {
      console.error("Lỗi khi tải workspace:", error);
      container.innerHTML = "<p>Không thể tải danh sách workspace.</p>";
    });
});
