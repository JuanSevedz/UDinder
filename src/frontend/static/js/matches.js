const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

    
function goHome() {
    window.location.href = "home.html"; // Here you must get the ID of the current user
}

async function seeMatches() {
    const userId = 1; // Here you must get the ID of the current user

    try {
        const response = await fetch(`${URL_BASE}/matches/${userId}`);
        const matches = await response.json();

        const matchesList = document.getElementById("matches-list");

        if (matches.length === 0) {
            matchesList.innerHTML = "<p>No matches found.</p>";
        } else {
            const matchesHTML = matches.map(match => `
                <div class="match">
                    <h3>${match.username}</h3>
                    <p>${match.description}</p>
                    <button class="button match-button" onclick="goToChat(${match.id})">Chat</button>
                </div>
            `).join("");

            matchesList.innerHTML = matchesHTML;
        }
    } catch (error) {
        console.error("Error fetching matches:", error);
        document.getElementById("matches-list").innerHTML = "<p>An error occurred while fetching matches.</p>";
    }
}

function goToChat(matchId) {
    window.location.href = `/chat?matchId=${matchId}`; // Here you must get the ID of the current user
}