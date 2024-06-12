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
            // Redirect user to login page
            window.location.href = "http://127.0.0.1:5500/src/frontend/templates/index.html"; // Change this URL to the login page
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

function showPhoto(userId) {
    fetch(`${URL_BASE}/profiles/show-photo/${userId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            const imageUrl = URL.createObjectURL(blob);
            const imageElement = document.getElementById("userPhoto");
            imageElement.src = imageUrl;
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle error here
        });
}

function showUserPhoto() {
    const userId = document.getElementById("userId").value;
    if (!userId) {
        alert("Please enter the User ID.");
        return;
    }
    showPhoto(userId);
}




function goProfilrDetail() {
    window.location.href = 'profile_detail.html';
}

function goMatches() {

    window.location.href = 'matches.html';

}


function goprofilesetup() {

    window.location.href = 'profile_setup.html';

}
function goSettings() {
    window.location.href = 'settings.html';
}

function closeWindow() {
    // close the actual window
    window.close();

    // If window.close() doesn't work (due to browser restrictions), redirect to a blank page
    window.location.href = "index.html";
}
async function like(userId, likedUserId) {
    try {
        const response = await fetch(`${URL_BASE}/like/${userId}/${likedUserId}`, {
            method: 'POST',
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById("result").innerText = data.message;
        } else {
            document.getElementById("result").innerText = data.detail;
        }
    } catch (error) {
        console.error("Error liking user:", error);
        document.getElementById("result").innerText = "An error occurred while liking the user.";
    }
}