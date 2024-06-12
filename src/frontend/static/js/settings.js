const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

function updateUserData() {
    const userId = document.getElementById("userId").value;
    const name = document.getElementById("name").value;
    const password = document.getElementById("password").value;
    const preferences = document.getElementById("preferences").value;
    const location = document.getElementById("location").value;

    const userData = {
        name: name,
        password: password,
        preferences: preferences,
        location: location
    };

    fetch(`${URL_BASE}/users/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update user data');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update user data');
        });
}

function goHome() {
    window.location.href = 'home.html';
}