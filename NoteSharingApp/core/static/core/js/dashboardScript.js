document.addEventListener("DOMContentLoaded", () => {
  const userProfileWidget = document.getElementById("userProfileWidget");
  const logoutButton = userProfileWidget.querySelector(".button");
  setTimeout(() => {
    userProfileWidget.classList.remove("expanded");
    userProfileWidget.classList.add("collapsed");
  }, 2000);
  
  function toggleUserProfileState() {
    if (userProfileWidget.classList.contains("collapsed")) {
      userProfileWidget.classList.remove("collapsed");
      userProfileWidget.classList.add("expanded");
    } else {
      userProfileWidget.classList.remove("expanded");
      userProfileWidget.classList.add("collapsed");
    }
  }
  
  userProfileWidget.addEventListener("click", (event) => {
    if (event.target !== logoutButton) {
      toggleUserProfileState();
    }
  });
  
  document.addEventListener("click", (event) => {
    if (
      userProfileWidget.classList.contains("expanded") &&
      !userProfileWidget.contains(event.target)
    ) {
      userProfileWidget.classList.remove("expanded");
      userProfileWidget.classList.add("collapsed");
    }
  });
  
  if (logoutButton) {
    logoutButton.addEventListener("click", (event) => {
      event.stopPropagation();
      alert("Logging out..."); // For demo
      // window.location.href = '{% url "logout" %}'; // Uncomment for actual Django logout
    });
  }
});