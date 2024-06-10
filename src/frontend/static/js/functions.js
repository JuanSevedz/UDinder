let URL_BASE = "http://localhost:8000"


// Hacer una solicitud GET a un endpoint de tu API
fetch('/api/endpoint')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

async function callMessage() {
    try {
        const response = await fetch(URL_BASE + '/hello_ud');
        const data = await response.text();
        document.getElementById('result').textContent = data;
    } catch (error) {
        console.error('Error:', error);
    }
}
async function showUsers() {
    try {
        const response = await fetch(URL_BASE + '/users/');
        const data = await response.json();

        let table = '<table>';
        table += '<tr><th>id</th><th>email</th><th>name</th><th>birth_date</th><th>preferences</th><th>location</th><th>age</th></tr>'; // Fixing typo in 'birth_date' and adding missing '<th>' tag before 'location'

        data.forEach(item =>{
            table += `<tr><td>${item.id}</td><td>${item.email}</td><td>${item.name}</td><td>${item.birth_date}</td><td>${item.preferences}</td><td>${item.location}</td></tr>`; // Using backticks for template string
        });
        table += '</table>';
        document.getElementById('result').innerHTML = table;

    } catch(error) {
        console.error('Error:', error);
    }
}


