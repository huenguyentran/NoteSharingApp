const csrftoken = getCookie('csrftoken');
const username = document.querySelector('#id_username');
const password = document.querySelector('#id_password');
const confirmPassword = document.querySelector('#id_confirm_password');
const usernameFeedbackArea = document.querySelector('.invalid-username-feedback');
const passwordFeedbackArea = document.querySelector('.invalid-password-feedbacks');

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

password.addEventListener('keyup', (e) => {
  const passwordValue = e.target.value; 
  password.classList.remove('is-invalid');
  passwordFeedbackArea.style.display = 'none';


  if (passwordValue.length > 0) {
    fetch("/auth/password-validation/", {
      method: "POST",
      headers:{
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken, 
      },
      body: JSON.stringify({ password: passwordValue }),
    })
    .then((res) => res.json())
    .then((data) => {
      if(data.password_error)
      {
        password.classList.add('is-invalid');
        passwordFeedbackArea.style.display = 'block';
        passwordFeedbackArea.innerHTML = `<p>${data.password_error}</p>`;
      }
    });
  }
});


username.addEventListener('keyup', (e) => {
  const usernameValue = e.target.value; 

  username.classList.remove('is-invalid');
  usernameFeedbackArea.style.display = 'none';

  if (usernameValue.length > 0) {
    fetch("/auth/username-validation/", {
      method: "POST",
      headers:{
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie('csrftoken'), 
      },
      body: JSON.stringify({ username: usernameValue }),
    })
    .then((res) => res.json())
    .then((data) => {
      if(data.username_error)
      {
        username.classList.add('is-invalid');
        usernameFeedbackArea.style.display = 'block';
        usernameFeedbackArea.innerHTML = `<p>${data.username_error}</p>`;

      }
    })
  }
});

