let jobListing = '';

function startInterview() {
    // Check if a job listing has been provided
    jobListing = document.getElementById('job-input').value;
    if (jobListing) {
        document.getElementById('start-interview-btn').disabled = true;

        // Start the loading indicator and progress bar
        document.querySelector('.loading').style.display = 'block';
        document.querySelector('.progress').style.display = 'block';
 
        // Call Flask API to start interview simulation with GPT
        fetch('/start-interview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_listing: jobListing })
        }).then(response => response.json())
        .then(data => {
            // Update progress indicator and chat display with initial messages from GPT
            document.querySelector('.loading').style.display = 'none';
            document.getElementById('progress-indicator').innerText = '100%';
            let chatDisplay = document.getElementById('chat-display');
            data['messages'].forEach(message => {
                let messageElement = document.createElement('div');
                messageElement.classList.add('chat-bubble');
                if (message['role'] === 'assistant') {
                    messageElement.classList.add('gpt-message');
                } else {
                    messageElement.classList.add('user-message');
                }
                messageElement.innerText = message['content'];
                chatDisplay.appendChild(messageElement);
            });
        })
        .catch(error => console.log(error));
    }
}

function sendMessage() {
    let userInput = document.getElementById('user-input').value;
    if (userInput) {
        // Call Flask API to send user message and receive GPT response
        fetch('/send-message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_listing: jobListing, user_input: userInput })
        }).then(response => response.json())
        .then(data => {
            // Update chat display with new message from GPT
            let chatDisplay = document.getElementById('chat-display');
            let messageElement = document.createElement('div');
            messageElement.classList.add('chat-bubble', 'gpt-message');
            messageElement.innerText = data['content'];
            chatDisplay.appendChild(messageElement);
        })
        .catch(error => console.log(error));
    }
}

function finishInterview() {
    // Call Flask API to finish interview simulation
    fetch('/finish-interview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_listing: jobListing })
    }).then(response => response.json())
    .then(data => {
        // Display completion message and next steps button
        let chatDisplay = document.getElementById('chat-display');
        let messageElement = document.createElement('div');
        messageElement.classList.add('completion-message');
        messageElement.innerText = 'Interview Completed. Click "Next Steps" to continue.';
        chatDisplay.appendChild(messageElement);
        
        // Enable the finish button and hide the start interview button
        document.getElementById('finish-interview-btn').disabled = false;
        document.getElementById('start-interview-btn').style.display = 'none';
    })
    .catch(error => console.log(error));
}
// Function to handle input changes and enable/disable the submit button
document.getElementById('user-input').addEventListener('input', function () {
    const submitButton = document.getElementById('submit-btn');
    submitButton.disabled = this.value.trim() === ''; // Disable if no text
});

