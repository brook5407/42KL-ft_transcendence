const host = window.location.hostname;
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const port = window.location.port || (protocol === 'wss:' ? '443' : '80');
const name = encodeURIComponent(nickname);

let currentUrl = window.location.href;
let url = new URL(currentUrl);
let group_num = url.searchParams.get('room');
// let group_num = {num};

if (!group_num) {
    group_num = 123;
}

const socketURL = `${protocol}//${host}:${port}/room/${ group_num }/?customer_name=${name}`;
// const socketURL = `${protocol}//${host}:${port}/room/123/?customer_name=${name}`;
// const socketURL = `${protocol}//${host}:${port}/room/{{ group_num }}/?customer_name=${name}`;

let socket = null;

function newSocket() {
    if (socket !== null && socket.readyState === WebSocket.OPEN) {
        socket.close();
    }

    socket = new WebSocket(socketURL);

    socket.onopen = function(event) {
        console.log("WebSocket connection opened.");
        let tag = document.createElement("div");
        tag.innerText = "连接成功";
        tag.style.color = "green";
        tag.append("\t你有朋友了 (｡♥‿♥｡) ");
        // document.querySelector(".message").appendChild(tag);
        message_sect = document.querySelector(".message")
        if (message_sect) {
            message_sect.appendChild(tag);
        }
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'message') {
            displayChatMessage(data.message);
        } else if (data.type === 'image') {
            displayImage(data.image, data.name);
            // displayImageMessage(data.image);
        }
        else {
            displayChatMessage(data.message);
        }
        scrollToBottom();
    };
    

    socket.onclose = function(event) {
        console.log("WebSocket connection closed.");
        logMessage(nickname + '连接已断开', 'error');
        let tag = document.createElement("div");
        tag.innerText = "连接关闭";
        tag.append("\t你没朋友了 ｡ﾟ･ (>﹏<) ･ﾟ｡ ");
        tag.style.color = "red";
        message_sect = document.querySelector(".message")
        if (message_sect.hasChildNodes()) {
            message_sect.appendChild(tag);
        }
    };

    socket.onerror = function(error) {
        console.error("WebSocket error:", error);
    };
}

function openConnect(){
    if (socket.readyState === WebSocket.OPEN)
        return;
    newSocket();
}

newSocket();

document.getElementById('fileInput').addEventListener('change', handleUpload);
function handleUpload() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function(event) {
            const imageUrl = event.target.result;

            // Display the uploaded image immediately
            // displayImage(imageUrl);

            // Send the image URL via WebSocket
            socket.send(JSON.stringify({
                'type': 'image',
                'name': nickname,
                'image': imageUrl
            }));
        };

        reader.readAsDataURL(file);
    } else {
        alert('Please select a file to upload.');
    }

}

// Display uploaded image
function displayImage(imageUrl, name) {
    const imageContainer = document.getElementById('message-container');
    const imgElement = document.createElement('img');
    imgElement.src = imageUrl;
    imgElement.style.maxWidth = '100px'; // Adjust styling as needed
    imgElement.style.display = 'inline-block';
    
    let username = document.createElement("div");
    username.innerText = name + " : ";
    username.style.color = "blue";
    imageContainer.appendChild(username);
    
    imgElement.onload = function() {
        imageContainer.appendChild(imgElement);
        // let username = document.createElement("div");
        // username.innerText = "\n";
        imageContainer.appendChild(document.createElement("div")).innerText = "\n";
        
        scrollToBottom();
    };

    imgElement.onerror = function() {
        // Remove the image element if it fails to load
        imgElement.remove();
        
        // Display an error message or a placeholder image
        const errorMessage = document.createElement("div");
        errorMessage.innerText = "Failed to load image";
        errorMessage.style.color = "red";
        imageContainer.appendChild(errorMessage);
        
        // Add a placeholder image if desired
        const placeholder = document.createElement('img');
        placeholder.src = 'static/images/meme/miku_impatient.png'; // Provide a valid path to a placeholder image
        placeholder.style.maxWidth = '100px';
        placeholder.style.display = 'inline-block';
        imageContainer.appendChild(placeholder);
        
        imageContainer.appendChild(document.createElement("div")).innerText = "\n";
        scrollToBottom();
    };


    // imageContainer.appendChild(document.createElement('br'));
}

function resizeImage(image) {
    const container = document.getElementById('imageContainer');
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size to container size
    canvas.width = container.offsetWidth;
    canvas.height = container.offsetHeight;

    // Calculate aspect ratio
    const scale = Math.min(canvas.width / image.width, canvas.height / image.height);
    const x = (canvas.width - image.width * scale) / 2;
    const y = (canvas.height - image.height * scale) / 2;

    // Draw the image on the canvas
    ctx.drawImage(image, x, y, image.width * scale, image.height * scale);

    // Convert canvas to data URL and set it as the image source
    const resizedImage = document.getElementById('resizedImage');
    resizedImage.src = canvas.toDataURL('image/jpeg');
}

// document.getElementById('uploadButton').addEventListener('click', () => {
//     const resizedImage = document.getElementById('resizedImage');
//     if (resizedImage.src) {
//         // Upload the resized image (data URL) to the server or handle it as needed
//         console.log('Image data URL:', resizedImage.src);

//         // Example of uploading the image:
//         // const formData = new FormData();
//         // formData.append('image', resizedImage.src);
//         // fetch('/upload', { method: 'POST', body: formData });
//     } else {
//         alert('No image to upload.');
//     }
// });

function sendMessage() {
    if (socket.readyState === WebSocket.OPEN) {
        let message = document.getElementById("txt").value.trim();
        if (message !== "") {
            socket.send(JSON.stringify({
                'type': 'message',
                'name': nickname,
                'message': message
            }));
            document.getElementById("txt").value = "";
        }
    } else {
        socket_state(socket);
        openConnect();
    }
}

const styles = {
    default: 'color: black;',
    warning: 'color: orange; font-weight: bold;',
    error: 'color: red; font-weight: bold;'
};

function logMessage(message, style = 'default') {
    console.log(`%c${message}`, styles[style]);
}

function socket_state(socket) {
    if (socket.readyState === WebSocket.OPEN) {
        logMessage('The connection is open', 'warning');
    } else if (socket.readyState === WebSocket.CONNECTING) {
        logMessage('The connection is connecting', 'warning');
    } else if (socket.readyState === WebSocket.CLOSING) {
        logMessage('The connection is closing', 'warning');
    } else if (socket.readyState === WebSocket.CLOSED) {
        logMessage('The connection is closed', 'warning');
    } else {
        logMessage('The connection state is unknown', 'warning');
    }
}

function scrollToBottom() {
    var messageContainer = document.getElementById('message-container');
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

function handleMessage(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function displayChatMessage(data) {
    let message = document.createElement("div");
    let messageText = data.trim();

    // Regular expression to split the message by the first colon
    let regex = /^([^:]*):(.*)$/;
    let match = regex.exec(messageText);

    if (match) {
        let textBeforeColon = document.createElement("span");
        textBeforeColon.textContent = match[1].trim();
        textBeforeColon.style.color = "blue"; // Example: change color to blue

        let textAfterColon = document.createElement("span");
        textAfterColon.textContent = match[2].trim();

        message.appendChild(textBeforeColon);
        message.appendChild(document.createTextNode(": ")); // Add colon separator
        message.appendChild(textAfterColon);
    } else {
        let textNode = document.createTextNode(messageText);
        message.appendChild(textNode);
    }

    document.querySelector(".message").appendChild(message);

    // Optionally, scroll to the bottom of the chat container
    // scrollToBottom();
}

function closeConnect(){
    socket.close(); //关闭连接 //向服务器发送断开连接的请求
}

var dataURLToBlob = function(dataURL) {
    var BASE64_MARKER = ';base64,';
    if (dataURL.indexOf(BASE64_MARKER) == -1) {
        var parts = dataURL.split(',');
        var contentType = parts[0].split(':')[1];
        var raw = parts[1];

        return new Blob([raw], {type: contentType});
    }

    var parts = dataURL.split(BASE64_MARKER);
    var contentType = parts[0].split(':')[1];
    var raw = window.atob(parts[1]);
    var rawLength = raw.length;

    var uInt8Array = new Uint8Array(rawLength);

    for (var i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }

    return new Blob([uInt8Array], {type: contentType});
}
