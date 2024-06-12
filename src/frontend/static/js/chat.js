const URL_BASE = "http://localhost:8000";

fetch(`${URL_BASE}/api/endpoint`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

function backHome(){
    window.location.href='home.html'
}

function sendMessage() {
    const senderId = document.getElementById('senderId').value;
    const receiverId = document.getElementById('receiverId').value;
    const messageContent = document.getElementById('messageContent').value;

    const data = {
        sender_id: senderId,
        receiver_id: receiverId,
        content: messageContent
    };

    fetch(`${URL_BASE}/messages/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Message sent:', data);
        document.getElementById('result').innerText = 'Message sent successfully!';
    })
    .catch((error) => {
        console.error('Error sending message:', error);
        document.getElementById('result').innerText = 'Error sending message.';
    });
}




   