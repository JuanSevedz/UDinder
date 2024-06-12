const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
    

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    } else {
        console.error(`Section with id '${sectionId}' not found.`);
    }
}

function goAdmin() {
    window.location.href = 'admin.html';
}

function goUser(){

window.location.href = 'user.html';

}

document.addEventListener("DOMContentLoaded", () => {
    const loginBtn = document.querySelector(".login-btn");

    loginBtn.addEventListener("click", () => {
        window.location.href = "http://127.0.0.1:5500/src/frontend/templates/login.html";
    });
});
