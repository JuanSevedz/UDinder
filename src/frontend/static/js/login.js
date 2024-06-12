const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

document.addEventListener("DOMContentLoaded", function() {
    createLoginForm();
});

async function createLoginForm() {
    let form = "";
    form += "<div class='login-form'>";
    form += "<div class='form-group'>";
    form += "<div class='label-box'>";
    form += "<label for='txtEmail' id='lblEmail'>Email</label>";
    form += "</div>"; 

    form += "<input type='email' id='txtEmail' required>";
    form += "</div>"; 

    form += "<div class='form-group'>";
    form += "<div class='label-box'>";
    form += "<label for='txtPassword' id='lblPassword'>Password</label>";
    form += "</div>"; 

    form += "<input type='password' id='txtPassword' required>";
    form += "</div>"; 

    form += "<div class='center-button'>";
    form += "<button type='button' onclick='loginUser()'>Login</button>";
    form += "<button type='button' onclick='goSignUp()'>Back to Sign up</button>";
    form += "</div>"; 
    form += "</div>"; 
    document.getElementById('result').innerHTML = form;
}


async function createLoginForm() {
    let form = "";
    form += "<div class='login-form'>";
    form += "<div class='form-group'>";
    form += "<div class='label-box'>";
    form += "<label for='txtEmail' id='lblEmail'>Email</label>";
    form += "</div>"; 

    form += "<input type='email' id='txtEmail' required>";
    form += "</div>"; 

    form += "<div class='form-group'>";
    form += "<div class='label-box'>";
    form += "<label for='txtPassword' id='lblPassword'>Password</label>";
    form += "</div>"; 

    form += "<input type='password' id='txtPassword' required>";
    form += "</div>"; 

    form += "<div class='center-button'>";
    form += "<button type='button' onclick='loginUser()'>Login</button>";
    form += "<button type='button' onclick='goSignUp()'>Back to Sign up</button>";
    form += "</div>"; 
    form += "</div>"; 
    document.getElementById('result').innerHTML = form;
}

async function loginUser() {
    let data = {
        email: document.getElementById('txtEmail').value,
        password: document.getElementById('txtPassword').value
    };
    
    try {
        const response = await fetch(`${URL_BASE}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (response.ok) {
            console.log("User authenticate:", result);
            alert("Login successful!");
            window.location.href = "http://127.0.0.1:5500/src/frontend/templates/home.html";
        } else {
            console.error("Error:", result.detail);
            alert("Invalid credentials");
        }
    } catch (error) {
        console.error('Error:', error);
        alert("An error occurred during login");
    }
}

function goSignUp() {
    window.location.href = 'sing_up.html';
}

createLoginForm();