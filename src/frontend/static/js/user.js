const URL_BASE = "http://localhost:8000";

fetch('/api/endpoint')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));


function goSing_in(){
    window.location.href = 'sing_in.html';

}
function goSing_up (){
    window.location.href = 'sing_up.html';

}
function goHome() {
    window.location.href = 'index.html';
}                                                                   