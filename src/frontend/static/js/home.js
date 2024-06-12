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

document.addEventListener("DOMContentLoaded", () => {
    const profileContainer = document.getElementById("profile-container");
    const profileCard = document.getElementById("profile-card");

    let initialX = null;

    profileCard.addEventListener("touchstart", (event) => {
        initialX = event.touches[0].clientX;
    });

    profileCard.addEventListener("touchmove", (event) => {
        if (initialX === null) {
            return;
        }

        const currentX = event.touches[0].clientX;
        const deltaX = currentX - initialX;

        if (deltaX > 0) {
            // Right swipe (interested)
            profileCard.style.transform = `translateX(${deltaX}px) rotate(30deg)`;
        } else {
            // Left swipe (not interested)
            profileCard.style.transform = `translateX(${deltaX}px) rotate(-30deg)`;
        }
    });

    profileCard.addEventListener("touchend", () => {
        profileCard.style.transition = "transform 0.5s ease-out";

        if (initialX > 100) {
            // Swipe right, handle interest
            profileCard.style.transform = "translateX(100%) rotate(30deg)";
            setTimeout(() => {
                // Fetch next profile
                // You can implement this part to load the next profile
                // For now, let's assume the profile is loaded instantly
                profileCard.style.transition = "none";
                profileCard.style.transform = "none";
            }, 500); // Delay for animation to finish
        } else if (initialX < -100) {
            // Swipe left, handle not interested
            profileCard.style.transform = "translateX(-100%) rotate(-30deg)";
            setTimeout(() => {
                // Fetch next profile
                profileCard.style.transition = "none";
                profileCard.style.transform = "none";
            }, 500);
        } else {
            // Reset position
            profileCard.style.transform = "none";
        }

        initialX = null;
    });
});
