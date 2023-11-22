function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    var chatDisplay = document.getElementById('chat-display');
    var newMessage = document.createElement('div');
    newMessage.textContent = userInput;
    chatDisplay.appendChild(newMessage);
    document.getElementById('user-input').value = '';
}

