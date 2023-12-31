// parse.js

var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('parser_message', function (msg) {
    var fileContent = document.getElementById('file-content');
    fileContent.value += '\n' + msg;
    scrollToBottom(); // Call scrollToBottom after appending new content
});

// Clear the text box on page load
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('file-content').value = '';
});

function loadFile() {
    var input = document.createElement('input');
    input.type = 'file';
    input.accept = '.txt,.json'; // accept both txt and json files
    input.onchange = function (event) {
        var file = event.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var contentType = file.type; // get the content type of the file
                var content = e.target.result;

                // check if it's a JSON file
                if (contentType === "application/json") {
                    // Send the JSON content to Flask for processing
                    fetch('/process_json', {
                        method: 'POST',
                        body: JSON.stringify({ content: content }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Failed to process file.');
                            }
                            return response.json();
                        })
                        .then(data => {
                            // Display the processed content in the text box
                            document.getElementById('file-content').value = data.processed_content.content;
                        })
                        .catch(error => {
                            console.error('Error processing file:', error);
                            document.getElementById('file-content').innerText = 'Error processing file.';
                        });
                }

                // If it's a text file, send the content to '/process_file' route
                else {
                    fetch('/process_file', {
                        method: 'POST',
                        body: JSON.stringify({ content: content }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Failed to process file.');
                            }
                            return response.json();
                        })
                        .then(data => {
                            // Display the processed content in the text box
                            document.getElementById('file-content').value = data.processed_content;
                        })
                        .catch(error => {
                            console.error('Error processing file:', error);
                            document.getElementById('file-content').innerText = 'Error processing file.';
                        });
                }
            };
            reader.readAsText(file);
        }
    };
    input.click();
}

function runCode() {
    // Display "parsing resume..." in the text box
    document.getElementById('file-content').value = 'Parsing resume...';

    // Call the Flask route to run the code
    fetch('/run_code')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to run code.');
            }
            return response.json();
        })
        .then(data => {
            // Display the result in the text box
            document.getElementById('file-content').value = data.result;
        })
        .catch(error => {
            console.error('Error running code:', error);
            document.getElementById('file-content').innerText = 'Error running code.';
        });
}

function downloadFile() {
    fetch('/download_parsed_resume')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to download parsed resume.');
            }
            return response.blob();
        })
        .then(blob => {
            saveAs(blob, 'parsed_resume.json');
        })
        .catch(error => {
            console.error('Error downloading parsed resume:', error);
            alert('Error downloading parsed resume.');
        });
}

// JavaScript code to instruct flask server to save the data in the session variable '/save_parsed_resume'
function saveFile() {
    fetch('/save_parsed_resume', { method: 'POST' });
}

// JavaScript code to scroll to the bottom of the text box
function scrollToBottom() {
    var fileContent = document.getElementById('file-content');
    fileContent.scrollTop = fileContent.scrollHeight;
}

