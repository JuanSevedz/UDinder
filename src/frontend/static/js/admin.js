const URL_BASE = "http://localhost:8000";

fetch('/api/endpoint')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

    
async function showUsers() {
    try {
        const response = await fetch(URL_BASE + '/users/');
        const data = await response.json();

        let table = '<table>';
        table += '<tr><th>id</th><th>email</th><th>name</th><th>birth_date</th><th>preferences</th><th>location</th><th>age</th></tr>'; // Fixing typo in 'birth_date' and adding missing '<th>' tag before 'location'

        data.forEach(item =>{
            table += `<tr><td>${item.id}</td><td>${item.email}</td><td>${item.name}</td><td>${item.birth_date}</td><td>${item.preferences}</td><td>${item.location}</td><td>${item.age}</td></tr>`; // Using backticks for template string
        });
        table += '</table>';
        document.getElementById('result').innerHTML = table;

    } catch(error) {
        console.error('Error:', error);
    }
}

async function showUserById(userId) {
    try {
        const response = await fetch(`${URL_BASE}/users/${userId}`);
        const user = await response.json();

        if (user) {
            let table = '<table>';
            table += '<tr><th>id</th><th>email</th><th>name</th><th>birth_date</th><th>preferences</th><th>location</th><th>age</th></tr>';

            table += `<tr><td>${user.id}</td><td>${user.email}</td><td>${user.name}</td><td>${user.birth_date}</td><td>${user.preferences}</td><td>${user.location}</td><td>${user.age}</td></tr>`;
            
            table += '</table>';
            document.getElementById('result').innerHTML = table;
        } else {
            document.getElementById('result').innerHTML = "No se encontró ningún usuario con el ID proporcionado.";
        }

    } catch(error) {
        console.error('Error:', error);
    }
}

function getUserInfo() {
    const userId = prompt("Ingresa el ID del usuario:");
    if (userId) {
        showUserById(userId);
    } else {
        alert("Por favor, ingresa un ID válido.");
    }
}
function goHome() {
    window.location.href = 'index.html';
}
