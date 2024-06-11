const URL_BASE = "http://localhost:8000";

fetch('/api/endpoint')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));


async function addUser() {
    let form = "";
    form += "<label for='txtId' id='lblId'>ID:</label>";
    form += "<input type='number' id='txtId'><br>";

    form += "<label for='txtEmail' id='lblEmail'>Email:</label>";
    form += "<input type='email' id='txtEmail' required><br>";

    form += "<label for='txtName' id='lblName'>Name:</label>";
    form += "<input type='text' id='txtName' required><br>";

    form += "<label for='txtPassword' id='lblPasswor'>Password:</label>";
    form += "<input type='text' id='txtPassword' required><br>";

    form += "<label for='txtGender' id='lblGender'>Gender:</label>";
    form += "<input type='text' id='txtGender' required><br>";
    

    form += "<label for='txtBirthDate' id='lblBirthDate'>Birth Date:</label>";
    form += "<input type='date' id='txtBirthDate' required><br>";

    form += "<label for='txtPreferences' id='lblPreferences'>Preferences:</label>";
    form += "<textarea id='txtPreferences' rows='3' required></textarea><br>";

    form += "<label for='txtLocation' id='lblLocation'>Location:</label>";
    form += "<input type='text' id='txtLocation' required><br>";
    
    form += "<button type='button' onclick='createUser()'>Send to DB</button>";
    form += "</form>";

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
            document.getElementById('result').textContent = `User created successfully. Age: ${result.age}`;
        } else {
            document.getElementById('result').textContent = `Error: ${result.detail}`;
        }
    } catch (error) {
        console.error('Error:', error);
    }
}