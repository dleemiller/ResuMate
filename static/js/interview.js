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


function displayUserMessage(message) {
    var messageBox = document.createElement('div');
    messageBox.className = 'chat-message user-message';
    messageBox.innerText = message;
    document.getElementById('chat-display').appendChild(messageBox);
}

function displayBotMessage(message) {
    var messageBox = document.createElement('div');
    messageBox.className = 'chat-message bot-message';
    messageBox.innerText = message;
    document.getElementById('chat-display').appendChild(messageBox);
}

$(document).ready(function(){
    // call the function here
    displayBotMessage('Hello!');
});


Dropzone.options.myAwesomeDropzone = {
    paramName: "file",
    maxFilesize: 2, 
    acceptedFiles: '.txt',
    dictDefaultMessage: "Drag a file here or click to upload",
    clickable: true,
    height: 'auto',
    init: function() {
        this.on("success", function(file, responseText) {
            let textArea = document.createElement('textarea');
            textArea.id = 'job-input';
            textArea.classList.add('form-control');
            textArea.readOnly = true;
            textArea.style.resize = 'none';
            textArea.style.height = '100%';
            textArea.textContent = responseText;

            let dropzoneArea = document.getElementById('my-awesome-dropzone');
            dropzoneArea.innerHTML = '';
            dropzoneArea.appendChild(textArea);
        });
    }
};
