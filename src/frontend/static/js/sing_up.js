const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));


    async function addUser() {
        let form = "<div class='new-user-form'>"; // Wrap the table in a div container
        form += "<table class='new-user-table'>";
        
    
        form += "<tr><td>ID:</td><td><input type='number' id='txtId'></td></tr>"; // ID field
        form += "<tr><td>Email:</td><td><input type='email' id='txtEmail' required></td></tr>"; // Email field
        form += "<tr><td>Name:</td><td><input type='text' id='txtName' required></td></tr>"; // Name field
        form += "<tr><td>Password:</td><td><input type='text' id='txtPassword' required></td></tr>"; // Password field
        form += "<tr><td>Gender:</td><td><input type='text' id='txtGender' required></td></tr>"; // Campo para el género
        form += "<tr><td>Birth Date:</td><td><input type='date' id='txtBirthDate' required></td></tr>"; // Date of birth field
        form += "<tr><td>Preferences:</td><td><textarea id='txtPreferences' rows='3' required></textarea></td></tr>"; // Field for preferences
        form += "<tr><td>Location:</td><td><input type='text' id='txtLocation' required></td></tr>"; // field for ubication
        form += "<tr><td>age:</td><td><input type='number' id='txtAge' required></td></tr>";
        form += "</table>";
        form += "<div class='center-button'><button type='button' onclick='createUser()'>Send to DB</button></div>"; // Button to send the data
    
        form += "</div>"; //close the div
    
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
