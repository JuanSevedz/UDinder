const URL_BASE = "http://localhost:8000";

fetch('/api/endpoint')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
    // Función para mostrar el formulario de inicio de sesión


    // Función para mostrar el formulario de inicio de sesión
function showLoginForm() {
    let form = "";
    form += "<label for='txtEmail' id='lblEmail'>Email:</label>";
    form += "<input type='email' id='txtEmail' required><br>";

    form += "<label for='txtPassword' id='lblPassword'>Password:</label>";
    form += "<input type='password' id='txtPassword' required><br>";
    
    form += "<button type='button' onclick='loginUser()'>Log In</button>";
    
    document.getElementById('login-form').innerHTML = form;
}

// Función para enviar los datos de inicio de sesión al servidor
function loginUser() {
    let email = document.getElementById('txtEmail').value;
    let password = document.getElementById('txtPassword').value;

    // Aquí puedes implementar la lógica para enviar los datos al servidor
    // y autenticar al usuario
    console.log("Email:", email);
    console.log("Password:", password);
}

// Llamar a la función para mostrar el formulario de inicio de sesión cuando se carga la página
showLoginForm();


    function goSing_up (){
        window.location.href = 'sing_up.html';
    
    }

    function login(){
        window.location.href = ''
        
    }
    function goHome(){
        window.location.href = 'index.html'

    }