const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));


function goSing_in(){
    window.location.href = 'login.html';

}
function goSing_up (){
    window.location.href = 'sing_up.html';

}
function goHome() {
    window.location.href = 'index.html';
}                                                                   