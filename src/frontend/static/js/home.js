const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));



async function logoutUser() {
    try {
        const response = await fetch(`${URL_BASE}/logout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
             }
        });

        const result = await response.json();

        if (response.ok) {
            console.log("Usuario desautenticado:", result);
            alert("Logout successful!");
                // Redirigir al usuario a la página de inicio de sesión
            window.location.href = "http://127.0.0.1:5500/src/frontend/templates/index.html"; // Cambia esta URL a la página de inicio de sesión
        } else {
            console.error("Error:", result.detail);
            alert("Error during logout");
        }
    } catch (error) {
        console.error('Error:', error);
        alert("An error occurred during logout");
    }
}