const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

    
async function showUsers() {
    try {
        const response = await fetch(URL_BASE + '/users/');
        const data = await response.json();

        let table = '<table>';
        table += '<tr><th>id</th><th>email</th><th>name</th><th>birth_date</th><th>preferences</th><th>location</th><th>age</th></tr>';

        data.forEach(item =>{
            table += `<tr><td>${item.id}</td><td>${item.email}</td><td>${item.name}</td><td>${item.birth_date}</td><td>${item.preferences}</td><td>${item.location}</td><td>${item.age}</td></tr>`; 
        });
        table += '</table>';
        document.getElementById('result').innerHTML = table;

    } catch(error) {
        console.error('Error:', error);
    }
}



async function getUserInfo() {
    const userId = prompt("Enter a valid ID");
    if (userId !== null) {
        if (!isNaN(userId) && parseInt(userId) == userId) {
            await showUserById(userId);
        } else {
            alert("Please enter a valid ID (integer).");
        }
    } else {
        alert("Please enter an ID.");
    }
}

async function showUserById(userId) {
    try {
        if (!isNaN(userId) && parseInt(userId) == userId) {
            const response = await fetch(`${URL_BASE}/users/${userId}`);
            if (response.ok) {
                const user = await response.json();
                let table = '<table>';
                table += '<tr><th>id</th><th>email</th><th>name</th><th>birth_date</th><th>preferences</th><th>location</th><th>age</th></tr>';

                table += `<tr><td>${user.id}</td><td>${user.email}</td><td>${user.name}</td><td>${user.birth_date}</td><td>${user.preferences}</td><td>${user.location}</td><td>${user.age}</td></tr>`;
                
                table += '</table>';
                document.getElementById('result').innerHTML = table;
            } else {
                document.getElementById('result').innerHTML = "No user found with the given ID.";
            }
        } else {
            document.getElementById('result').innerHTML = "Please enter a valid ID (integer).";
        }
    } catch(error) {
        console.error('Error:', error);
    }
}
async function deleteUserById(userId) {
    try {
        const response = await fetch(`${URL_BASE}/users/${userId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data.message); 
        } else {
            const errorData = await response.json();
            console.error('Error:', errorData.detail); 
        }
    } catch(error) {
        console.error('Error:', error);
    }
}
async function deleteUserInfo() {
    const userId = prompt("Enter the ID of the user to delete:");
    if (userId !== null) {
        if (!isNaN(userId) && parseInt(userId) == userId) {
            await deleteUserById(userId);
        } else {
            alert("Please enter a valid ID (integer).");
        }
    } else {
        alert("Please enter an ID.");
    }
}
async function deleteMatchById(matchId) {
    try {
        const response = await fetch(`${URL_BASE}/matches/${matchId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data.message); 
            const errorData = await response.json();
            console.error('Error:', errorData.detail); 
        }
    } catch(error) {
        console.error('Error:', error);
    }
}


async function deleteMatchInfo() {
    const matchId = prompt("Enter the ID of the match to delete:");
    if (matchId !== null) {
        if (!isNaN(matchId) && parseInt(matchId) == matchId) {
            await deleteMatchById(matchId);
        } else {
            alert("Please enter a valid ID (integer).");
        }
    } else {
        alert("Please enter an ID.");
    }
}

// Función para 
async function deleteMatchById(matchId) {
    try {
        const response = await fetch(`${URL_BASE}/matches/${matchId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data.message); 
            document.getElementById('result').innerText = "Match deleted successfully"; 
        } else {
            const errorData = await response.json();
            if (response.status === 404) {
                console.error('Error:', errorData.detail); 
                document.getElementById('result').innerText = "No match found with the given ID"; 
            } else {
                console.error('Error:', errorData.detail); 
                document.getElementById('result').innerText = "An error occurred while deleting the match"; 
            }
        }
    } catch(error) {
        console.error('Error:', error);
        document.getElementById('result').innerText = "An error occurred while deleting the match"; 
    }
}

function promptDeleteMessage() {
    
    const messageId = window.prompt("Enter Message ID:");

    if (!messageId) {
       
        return;
    }

    fetch(`${URL_BASE}/messages/${messageId}/`, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        alert("Message deleted successfully.");
    })
    .catch((error) => {
        console.error('Error:', error);
        
        alert("An error occurred while deleting the message.");
    });
}


function goHome() {
    window.location.href = 'index.html';
}
