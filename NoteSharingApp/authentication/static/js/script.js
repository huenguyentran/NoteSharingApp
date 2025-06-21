
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.querySelector('.container');

signUpButton.addEventListener('click', () => {
    container.classList.add('right-panel-active');
});

signInButton.addEventListener('click', () => {
    container.classList.remove('right-panel-active');
});

document.addEventListener('DOMContentLoaded', (event) => {
    const registerForm = document.querySelector('.sign-up-container form');
    const loginForm = document.querySelector('.sign-in-container form');
    const messages = document.querySelectorAll('.messages li.error'); 
    let hasRegisterError = false;
    if (registerForm && registerForm.querySelector('.errorlist')) {
        hasRegisterError = true;
    }

    if (hasRegisterError && !container.classList.contains('right-panel-active')) {
        container.classList.add('right-panel-active');
    }
});