// static/js/chat.js
document.getElementById('send-message').addEventListener('click', function() {
    var conversationId = document.getElementById('conversation-id').value;
    var messageText = document.getElementById('message-text').value;

    fetch('/users/send_message_ajax/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            conversation_id: conversationId,
            text: messageText
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            var chatMessages = document.getElementById('chat-messages');
            var newMessage = document.createElement('div');
            newMessage.classList.add('chat-message');
            newMessage.classList.add('sent');
            newMessage.innerHTML = `<p>${data.message.sender}: ${data.message.body}</p><span class="timestamp">${data.message.timestamp}</span>`;
            chatMessages.appendChild(newMessage);
            document.getElementById('message-text').value = '';
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
