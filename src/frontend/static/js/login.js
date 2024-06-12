const URL_BASE = "http://localhost:8000";

// Función para crear la tabla de inicio de sesión
// Función para crear la tabla de inicio de sesión
// Función para crear la tabla de inicio de sesión
async function createLoginForm() {
    let form = "";
    form += "<div class='login-form'>";
    form += "<div class='form-group'>";
    form += "<div class='label-box'>";
    form += "<label for='txtEmail' id='lblEmail'>Email</label>";
    form += "</div>"; // Cierra la caja de la etiqueta

    form += "<input type='email' id='txtEmail' required>";
    form += "</div>"; // Cierra el grupo de formulario

    form += "<div class='form-group'>";
    form += "<div class='label-box'>";
    form += "<label for='txtPassword' id='lblPassword'>Password</label>";
    form += "</div>"; // Cierra la caja de la etiqueta

    form += "<input type='password' id='txtPassword' required>";
    form += "</div>"; // Cierra el grupo de formulario

    form += "<div class='center-button'>";
    form += "<button type='button' onclick='loginUser()'>Login</button>";
    form += "<button type='button' onclick='goSignUp()'>Back to Sign up</button>";
    form += "</div>"; // Cierra el div del botón centrado

    form += "</div>"; // Cierra el div de formulario de inicio de sesión

    document.getElementById('result').innerHTML = form;
}


// Función para enviar los datos de inicio de sesión al servidor
async function loginUser() {
    let data = {
        email: document.getElementById('txtEmail').value,
        password: document.getElementById('txtPassword').value
    };
    
    // Realiza la lógica de autenticación con los datos proporcionados
    
    // Puedes hacer una petición fetch al servidor para realizar la autenticación
    // Aquí va tu código de autenticación

    // Simulando una petición exitosa por ahora
    console.log("Usuario autenticado:", data);
}

// Función para ir a la página de registro de usuario (sing_up.html)
function goSignUp() {
    window.location.href = 'sing_up.html';
}
