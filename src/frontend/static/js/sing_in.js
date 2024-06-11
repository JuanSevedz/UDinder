const URL_BASE = "http://localhost:8000";

fetch('/api/endpoint')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

    function goSing_up (){
        window.location.href = 'sing_up.html';
    
    }

    function login(){
        window.location.href = ''
        
    }
    function goHome(){
        window.location.href = 'index.html'

    }