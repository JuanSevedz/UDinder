const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

function goHome() {
    window.location.href = 'home.html';
}

function showForm(formId) {
    const forms = ['upload-form', 'description-form', 'interests-form'];
    forms.forEach(id => {
        document.getElementById(id).style.display = (id === formId) ? 'block' : 'none';
    });
}

function uploadPhoto() {
    const userId = document.getElementById("upload-user-id").value;
    const photo = document.getElementById("photo").files[0];
    
    if (!userId) {
        alert("Please enter the User ID.");
        return;
    }

    if (!photo) {
        alert("Please select a photo to upload.");
        return;
    }

    const formData = new FormData();
    formData.append("photo", photo);

    fetch(`${URL_BASE}/profiles/upload-photo/?user_id=${userId}`, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerText = data.message;
        
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function addDescription() {
    const userId = document.getElementById("description-user-id").value;
    const description = document.getElementById("description").value;

    if (!userId) {
        alert("Please enter the User ID.");
        return;
    }

    if (!description) {
        alert("Please enter a description.");
        return;
    }

    const params = new URLSearchParams();
    params.append('description', description);

    fetch(`${URL_BASE}/profiles/add-description/?user_id=${userId}`, {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function setInterests() {
    const userId = document.getElementById("interests-user-id").value;
    const interests = document.getElementById("interests").value;

    if (!userId) {
        alert("Please enter the User ID.");
        return;
    }

    if (!interests) {
        alert("Please enter interests.");
        return;
    }

    const params = new URLSearchParams();
    params.append('interests', interests);

    fetch(`${URL_BASE}/profiles/set-interests/?user_id=${userId}`, {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

async function logOut() {
    try {
        const response = await fetch('/logout', {
            method: 'POST'
        });

        if (response.ok) {
            const result = await response.json();
            document.getElementById("result").innerText = result.message;
            window.location.href = "login.html"; 
        } else {
            const error = await response.json();
            document.getElementById("result").innerText = error.detail;
        }
    } catch (error) {
        console.error("Error logging out:", error);
        document.getElementById("result").innerText = "An error occurred while logging out.";
    }
}
