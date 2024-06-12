const URL_BASE = "http://localhost:8000";

fetch('/api/endpoint')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));


function goAdmin() {
    window.location.href = 'admin.html';
}

function goUser(){

window.location.href = 'user.html';

    }

    function goLogin(){
        window.location.href = 'login.html'
        
    }

