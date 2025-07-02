document.addEventListener('DOMContentLoaded', function () {
  const csrftoken = getCookie('csrftoken');
  const username = document.querySelector('#id_res_username');
  const password = document.querySelector('#id_res_password');
  const confirmPassword = document.querySelector('#id_res_confirm_password');
  const usernameFeedbackArea = document.querySelector('.invalid-username-feedback');
  const passwordFeedbackArea = document.querySelector('.invalid-password-feedback');
  const registerBtn = document.getElementById('registerBtn');

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

  function showMessage(type, message) {
    const box = document.getElementById("message-area");
    if (!box) return;

    const li = document.createElement("li");
    li.classList.add(type);
    li.textContent = message;
    box.innerHTML = ""; // Clear old messages
    box.appendChild(li);

    setTimeout(() => {
        box.innerHTML = "";
    }, 2000);
  }

  if (password && passwordFeedbackArea) {
    password.addEventListener('keyup', (e) => {
      const passwordValue = e.target.value;
      password.classList.remove('is-invalid');
      passwordFeedbackArea.classList.remove('show');

      if (passwordValue.length > 0) {
        fetch("/auth/password-validation/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({ password: passwordValue }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.password_error) {
              password.classList.add('is-invalid');
              passwordFeedbackArea.classList.add('show');
              passwordFeedbackArea.innerHTML = `<p>${data.password_error}</p>`;
            }
          });
      }
    });
  }

  if (username && usernameFeedbackArea) {
    username.addEventListener('keyup', (e) => {
      const usernameValue = e.target.value;
      username.classList.remove('is-invalid');
      usernameFeedbackArea.classList.remove('show')

      if (usernameValue.length > 0) {
        fetch("/auth/username-validation/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({ username: usernameValue }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.username_error) {
              username.classList.add('is-invalid');
              usernameFeedbackArea.classList.add('show')
              usernameFeedbackArea.innerHTML = `<p>${data.username_error}</p>`;
            }
          });
      }
    });
  }

  registerBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const passwordValue = password.value;
    const confirmPasswordValue = confirmPassword.value;
    const registration_form = document.getElementById('registration_form');

    if(!password.classList.contains('is-invalid') && !username.classList.contains('is-invalid'))
    {
      fetch("/auth/registration-validation/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ password: passwordValue, confirmPassword : confirmPasswordValue }),
      })
      .then(res => res.json())
      .then(data => {
        if (data.validation_error) {
          showMessage("error", data.validation_error);
        } else  {
          showMessage("success", "Registration successful!");
          registration_form.submit();
        }
      });
    }
    else{
      showMessage("error", 'Invalid username or password');
    }

  });



  // Switch UI panel
  const signUpButton = document.getElementById('signUp');
  const signInButton = document.getElementById('signIn');
  const container = document.querySelector('.container');

  if (signUpButton && container) {
    signUpButton.addEventListener('click', () => {
      container.classList.add('right-panel-active');
    });
  }

  if (signInButton && container) {
    signInButton.addEventListener('click', () => {
      container.classList.remove('right-panel-active');
    });
  }

  // Check form errors and switch to correct panel
  const registerForm = document.querySelector('.sign-up-container form');
  const hasRegisterError = registerForm && registerForm.querySelector('.errorlist');
  if (hasRegisterError && container && !container.classList.contains('right-panel-active')) {
    container.classList.add('right-panel-active');
  }
});