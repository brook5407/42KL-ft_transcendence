const host = window.location.hostname;
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const port = window.location.port || (protocol === 'wss:' ? '443' : '80');

const appConfigElement = document.getElementById('chat-config');
const nickname = appConfigElement.getAttribute('data-nickname');
const groupNum = appConfigElement.getAttribute('data-room') || '0000';
// const groupNum = appConfigElement.getAttribute('data-room') || 'private_temp';
const receiver = appConfigElement.getAttribute('data-receiver') || null;

let socketURL = `${protocol}//${host}:${port}/room/${groupNum}/?customer_name=${nickname}`;
let socket = null;

document.getElementById('message-input').addEventListener('keydown', handleMessage);

function reconnectWebSocket() {
    let retries = 0;
    const maxRetries = 5; // Maximum number of retries

    function tryReconnect() {
        if (retries >= maxRetries) {
            console.error('Max reconnect attempts reached. Giving up.');
            return;
        }
        retries++;
        console.log(`Reconnecting... (Attempt ${retries}/${maxRetries})`);
        newSocket();
    }

    socket.onclose = function(event) {
        console.log('WebSocket connection closed. Attempting to reconnect...');
        setTimeout(tryReconnect, 3000); // Retry after 3 seconds
    };
}


function newSocket() {
    if (socket !== null && socket.readyState === WebSocket.OPEN) {
        socket.close();
    }
    socketURL = `${protocol}//${host}:${port}/room/${groupNum}/?customer_name=${nickname}`;
    socket = new WebSocket(socketURL);

    socket.onopen = handleSocketOpen;
    socket.onmessage = handleSocketMessage;
    socket.onclose = handleSocketClose;
    socket.onerror = handleSocketError;
}

function openConnect() {
    if (socket.readyState !== WebSocket.OPEN) {
        newSocket();
    }
}

function closeConnect() {
    if (socket) {
        socket.close(); // Close the connection
    }
}

function handleSocketOpen() {
    console.log('WebSocket connection opened.');
    appendStatusMessage('Connected', 'green', 'You have friends now (｡♥‿♥｡)');
}

function handleSocketMessage(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'message') {
        displayChatMessage(data.message, data.name);
    } else if (data.type === 'image') {
        displayImage(data.image, data.name);
    } else {
        console.warn('Unknown message type:', data.type);
    }
    scrollToBottom();
}

function handleSocketClose() {
    console.log('WebSocket connection closed.');
    logMessage(nickname + ' disconnected', 'error');
    appendStatusMessage('Disconnected', 'red', 'You have no friends now ｡ﾟ･ (>﹏<) ･ﾟ｡');
}

function handleSocketError(error) {
    console.error('WebSocket error:', error);
}

function handleMessage(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    if (socket.readyState === WebSocket.OPEN) {
        const message = document.getElementById('message-input').value.trim();
        if (message !== '') {
            socket.send(JSON.stringify({
                room_id: groupNum,
                type: 'message',
                name: nickname,
                message: message,
            }));
            document.getElementById('message-input').value = '';
        }
    } else {
        socket_state(socket);
        reconnectWebSocket();
    }
}

function displayChatMessage(message, name) {
    if (typeof message !== 'string') {
        console.error('Invalid input: expected a string.');
        return;
    }

    const messageContainer = document.querySelector('.chat-messages');
    const messageElement = document.createElement('div');
    messageElement.style.display = 'flex';
    messageElement.style.padding = '0 0 5px 0';
    messageElement.style.lineHeight = '1.3';
    messageElement.style.width = '100%';

    const username = document.createElement('span');
    username.textContent = `${name}:`;
    username.style.color = 'blue';
    username.style.fontWeight = 'bold';
    username.style.marginRight = '10px';

    const messageText = document.createElement('span');
    messageText.classList.add('chat-text');
    messageText.innerHTML = message;

    messageElement.appendChild(username);
    messageElement.appendChild(messageText);
    messageContainer.appendChild(messageElement);
}

function displayImage(imageUrl, name) {
    const imageContainer = document.getElementById('chat-messages');
    const messageWrapper = document.createElement('div');
    messageWrapper.style.display = 'flex';
    messageWrapper.style.padding = '0 0 5px 0';

    const username = document.createElement('span');
    username.textContent = name.endsWith(':') ? name : `${name}:`;
    username.style.color = 'blue';
    username.style.fontWeight = 'bold';
    username.style.marginRight = '10px';

    const imgElement = document.createElement('img');
    imgElement.src = imageUrl;
    imgElement.style.maxWidth = '80px';
    imgElement.style.height = 'auto';

    const placeholderUrl = 'static/images/meme/miku_impatient.png';
    const placeholder = document.createElement('img');
    placeholder.src = placeholderUrl;
    placeholder.style.maxWidth = '100px';
    placeholder.style.height = 'auto';
    placeholder.style.display = 'none';

    messageWrapper.appendChild(username);
    messageWrapper.appendChild(imgElement);
    messageWrapper.appendChild(placeholder);
    imageContainer.appendChild(messageWrapper);

    imgElement.onload = () => {
        placeholder.style.display = 'none';
        scrollToBottom();
    };

    imgElement.onerror = () => {
        imgElement.style.display = 'none';
        placeholder.style.display = 'inline-block';
        const errorMessage = document.createElement('div');
        errorMessage.innerText = 'Failed to load image';
        errorMessage.style.color = 'red';
        imageContainer.appendChild(errorMessage);
        scrollToBottom();
    };
}

function appendStatusMessage(status, color, message) {
    const tag = document.createElement('div');
    tag.innerText = status;
    tag.style.color = color;
    tag.append(`\t${message}`);
    document.querySelector('.chat-messages').appendChild(tag);
}

function scrollToBottom() {
    const messageContainer = document.getElementById('chat-messages');
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

function logMessage(message, style = 'default') {
    const styles = {
        default: 'color: black;',
        warning: 'color: orange; font-weight: bold;',
        error: 'color: red; font-weight: bold;',
    };
    console.log(`%c${message}`, styles[style]);
}

function socket_state(socket) {
    const stateMessages = {
        [WebSocket.OPEN]: 'The connection is open',
        [WebSocket.CONNECTING]: 'The connection is connecting',
        [WebSocket.CLOSING]: 'The connection is closing',
        [WebSocket.CLOSED]: 'The connection is closed',
    };
    const state = socket.readyState;
    const message = stateMessages[state] || 'The connection state is unknown';
    logMessage(message, 'warning');
}

// openConnect();
newSocket();
// reconnectWebSocket();
