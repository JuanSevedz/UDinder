const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));


    async function addUser() {
        let form = "<div class='new-user-form'>"; // Envuelve la tabla en un contenedor div
        form += "<table class='new-user-table'>";
        
    
        form += "<tr><td>ID:</td><td><input type='number' id='txtId'></td></tr>"; // Campo para el ID
        form += "<tr><td>Email:</td><td><input type='email' id='txtEmail' required></td></tr>"; // Campo para el email
        form += "<tr><td>Name:</td><td><input type='text' id='txtName' required></td></tr>"; // Campo para el nombre
        form += "<tr><td>Password:</td><td><input type='text' id='txtPassword' required></td></tr>"; // Campo para la contraseña
        form += "<tr><td>Gender:</td><td><input type='text' id='txtGender' required></td></tr>"; // Campo para el género
        form += "<tr><td>Birth Date:</td><td><input type='date' id='txtBirthDate' required></td></tr>"; // Campo para la fecha de nacimiento
        form += "<tr><td>Preferences:</td><td><textarea id='txtPreferences' rows='3' required></textarea></td></tr>"; // Campo para las preferencias
        form += "<tr><td>Location:</td><td><input type='text' id='txtLocation' required></td></tr>"; // Campo para la ubicación
        form += "<tr><td>age:</td><td><input type='number' id='txtAge' required></td></tr>";
        form += "</table>";
        form += "<div class='center-button'><button type='button' onclick='createUser()'>Send to DB</button></div>"; // Botón para enviar los datos
    
        form += "</div>"; // Cierra el contenedor div
    
        document.getElementById('result').innerHTML = form;
    }
    
    

// Function to send user data to the server
async function createUser() {
    let data = {
        id: document.getElementById('txtId').value, // Add the ID field provided by the user
        email: document.getElementById('txtEmail').value,
        name: document.getElementById('txtName').value,
        password: "string", // Enter the appropriate value for the password
        gender: "string", // Enter the user's gender if relevant, otherwise you can leave it as "string"
        birth_date: document.getElementById('txtBirthDate').value,
        preferences: document.getElementById('txtPreferences').value,
        location: document.getElementById('txtLocation').value,
        age: 0 // You can leave it as 0 if the age is calculated on the backend or remove it if it's generated automatically
    };
    console.log(data);

    let url_post = URL_BASE + '/users/add';

    try {
        const response = await fetch(url_post, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://localhost:5500',
                'Access-Control-Allow-Methods': 'POST'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (response.ok) {
            document.getElementById('result').textContent = `User created successfully`;
        } else {
            document.getElementById('result').textContent = `Error: ${result.detail}`;
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
