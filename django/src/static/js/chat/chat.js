// friendroom.js


// let { host, protocol, port } = window.getWebSocketConfig();
// let { nickname, roomId } = window.getChatConfig();

// let socketURL = `${protocol}//${host}:${port}/drawer/chat-friendroom/${roomId}/?customer_name=${nickname}`;

// console.log(`Connecting to ${socketURL}`);

// let connections = new Map(); // To store WebSocket connections by room ID
// let socket = null;

// document.getElementById('message-input').addEventListener('keydown', handleMessage);
// document.getElementById('send-button').addEventListener('click', sendMessage);

// if (!roomId) {
//     console.error('Room ID is missing');
// }



// import * as myModule from './chatConfig.js';
// import { host, protocol, port, nickname, roomId } from './chatConfig.js';
import { getWebSocketConfig, getChatConfig } from './chatConfig.js';



let connections = new Map(); // To store WebSocket connections by room ID
let host, protocol, port, nickname, roomId = null;
let socket = null;
let socketURL = null;

// const{ host, protocol, port } = window.getWebSocketConfig();
// const{ nickname, roomId } = window.getChatConfig();
document.addEventListener('drawer-opened', () => {
    var { host, protocol, port } = getWebSocketConfig();
    var { nickname, roomId } = getChatConfig();
    host = host;
    protocol = protocol;
    port = port;
    nickname = nickname;
    roomId = roomId;


    // Get configuration data from functions

    // Log configuration for debugging
    console.log(`Room ID: ${roomId}`);
    console.log(`Nickname: ${nickname}`);

    // Validate configurations
    if (!roomId) {
        console.error('Room ID is missing or not defined.');
        return;
    }
    if (!nickname) {
        console.error('Nickname is missing or not defined.');
        return;
    }

    // Create the WebSocket URL
    socketURL = `${protocol}//${host}:${port}/drawer/chat-friendroom/${roomId}/?customer_name=${nickname}`;
    console.log(`Connecting to ${socketURL}`);

    // Initialize connections map and WebSocket
    // let connections = new Map(); // To store WebSocket connections by room ID
    // let socket = null;

    // Set up event listeners for message input and send button
    document.getElementById('message-input').addEventListener('keydown', handleMessage);
    document.getElementById('send-button').addEventListener('click', sendMessage);

    // Connect to the specified room
    // socketURL = createSocketURL(roomId, protocol, nickname, port, host);
    connectToRoom(roomId);
    // disconnectFromRoom(roomId);
});








function createSocketURL(roomId) {
    if (!roomId) {
        console.error('Invalid room ID');
        return '';
    }
    console.log(`Creating socket URL for room': ${roomId}`);
    return `${protocol}//${host}:${port}/drawer/chat-friendroom/${roomId}/?customer_name=${nickname}`;
}

function connectToRoom(roomId) {
    if (!roomId) {
        console.error('Room ID is required to connect');
        return;
    }
    if (connections.has(roomId)) {
        console.log(`Already connected to room ${roomId}`);
        return;
    }
    // socketURL = createSocketURL(roomId, protocol, nickname);
    if (socket === null) {
            socket = new WebSocket(socketURL);
        }
    // socket = new WebSocket(socketURL);

    socket.onopen = () => handleSocketOpen(roomId);
    socket.onmessage = (event) => handleSocketMessage(event, roomId);
    socket.onclose = () => handleSocketClose(roomId);
    socket.onerror = handleSocketError;

    connections.set(roomId, socket);
    console.log(`Connecting to room ${roomId}`);
}

function disconnectFromRoom(roomId) {
    socket = connections.get(roomId);
    if (socket) {
        socket.close();
        connections.delete(roomId);
        console.log(`Disconnected from room ${roomId}`);
    }
}

function handleSocketOpen(roomId) {
    console.log(`WebSocket connection opened for room ${roomId}`);
    appendStatusMessage(roomId, 'Connected', 'green', `You are now connected to room ${roomId}`);
}

function handleSocketMessage(event, roomId) {
    const data = JSON.parse(event.data);
    if (data.type === 'message') {
        displayChatMessage(data.message, data.name, roomId);
    } else if (data.type === 'image') {
        displayImage(data.image, data.name, roomId);
    } else {
        console.warn('Unknown message type:', data.type);
    }
    scrollToBottom();
}

function handleSocketClose(roomId) {
    console.log(`WebSocket connection closed for room ${roomId}`);
    appendStatusMessage(roomId, 'Disconnected', 'red', `You have been disconnected from room ${roomId}`);
    connections.delete(roomId);
    reconnectWebSocket(roomId);
}

function handleSocketError(error) {
    console.error('WebSocket error:', error);
}

function reconnectWebSocket(roomId) {
    let retries = 0;
    const maxRetries = 5; // Maximum number of retries

    function tryReconnect() {
        if (retries >= maxRetries) {
            console.error('Max reconnect attempts reached. Giving up.');
            return;
        }
        retries++;
        console.log(`Reconnecting to room ${roomId}... (Attempt ${retries}/${maxRetries})`);
        connectToRoom(roomId);
    }

    setTimeout(tryReconnect, 3000); // Retry after 3 seconds
}

function handleMessage(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    const message = document.getElementById('message-input').value.trim();
    // console.log(`Sending message: ${message}`);  // Debugging line
    if (message !== '') {
        // const roomId = appConfigElement.getAttribute('data-room'); // Get the current room ID
        // const socket = connections.get(roomId);
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                room_id: roomId,
                type: 'message',
                name: nickname,
                message: message,
                // receiver_id: roomId,
            }));
            document.getElementById('message-input').value = '';
        } else {
            socket_state(socket);
            reconnectWebSocket(roomId);
        }
    }
}

function displayChatMessage(message, name, roomId) {
    if (typeof message !== 'string') {
        console.error('Invalid input: expected a string.');
        return;
    }

    const messageContainer = document.querySelector(`.chat-messages[data-room="${roomId}"]`);
    // const messageContainer = document.querySelector('.chat-messages');
    if (!messageContainer) return; // Ensure the message container exists

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

    console.log(`Displaying message: ${message}`);  // Debugging line
    messageElement.appendChild(username);
    messageElement.appendChild(messageText);
    messageContainer.appendChild(messageElement);
}

function displayImage(imageUrl, name, roomId) {
    const imageContainer = document.querySelector(`.chat-messages[data-room="${roomId}"]`);
    // const imageContainer = document.querySelector('.chat-messages');
    if (!imageContainer) return; // Ensure the message container exists

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

function appendStatusMessage(roomId, status, color, message) {
    const tag = document.createElement('div');
    tag.innerText = status;
    tag.style.color = color;
    tag.append(`\t${message}`);
    const messageContainer = document.querySelector(`.chat-messages[data-room="${roomId}"]`);
    // const messageContainer = document.querySelector('.chat-messages');
    if (messageContainer) {
        messageContainer.appendChild(tag);
    }
}

function scrollToBottom() {
    const messageContainers = document.querySelectorAll('.chat-messages');
    messageContainers.forEach(container => container.scrollTop = container.scrollHeight);
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
    const state = socket?.readyState;
    const message = stateMessages[state] || 'The connection state is unknown';
    logMessage(message, 'warning');
}

// function updateChatMessages(messages) {
//     const chatMessagesContainer = document.getElementById('chat-messages');
//     chatMessagesContainer.innerHTML = ''; // Clear existing messages

//     messages.forEach(message => {
//         const messageDiv = document.createElement('div');
//         messageDiv.className = 'chat-message';
//         messageDiv.innerHTML = `
//             <span class="chat-username">${message.sender.username}:</span>
//             <span class="chat-text">${message.text}</span>
//             ${message.image_url ? `<div class="chat-image"><img src="${message.image_url}" alt="Image message"></div>` : ''}
//             ${message.timestamp ? `<span class="chat-timestamp">${new Date(message.timestamp).toLocaleTimeString()}</span>` : ''}
//         `;
//         chatMessagesContainer.appendChild(messageDiv);
//     });
//     chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;

// }







// const chatList = document.querySelector('.friendroom-list');

// chatList?.addEventListener('click', (e) => {
//     const chatListItem = e.target.closest('.chat-container');

//     if (chatListItem) {
//         const roomId = chatListItem.getAttribute('data-roomid');
//         openDrawer('chat-room', {
//             url: chatListItem.getAttribute('data-drawer-url'),
//             state: {
//                 roomId
//             }
//     });
//     }
// });

// document.addEventListener('DOMContentLoaded', () => {
//     // const appConfigElement = document.getElementById('chat-config');
//     // const nickname = appConfigElement.getAttribute('data-nickname');
//     // const roomId = appConfigElement.getAttribute('data-room');

//     console.log(`Room ID: ${roomId}`);  // Debugging line
//     console.log(`Nickname: ${nickname}`);  // Debugging line

//     if (!roomId) {
//         console.error('Room ID is missing or not defined.');
//         return;
//     }

//     connectToRoom(roomId);
// });


// document.addEventListener('drawer-opened', () => {
//     let { host, protocol, port } = window.getWebSocketConfig();
//     let { nickname, roomId } = window.getChatConfig();

//     let socketURL = `${protocol}//${host}:${port}/drawer/chat-friendroom/${roomId}/?customer_name=${nickname}`;

//     console.log(`Connecting to ${socketURL}`);

//     let connections = new Map(); // To store WebSocket connections by room ID
//     let socket = null;

//     document.getElementById('message-input').addEventListener('keydown', handleMessage);
//     document.getElementById('send-button').addEventListener('click', sendMessage);

//     if (!roomId) {
//         console.error('Room ID is missing');
//     }
//     // const appConfigElement = document.getElementById('chat-config');
//     // const nickname = appConfigElement?.getAttribute('data-nickname');
//     // const roomId = appConfigElement?.getAttribute('data-room');

//     console.log(`Room ID: ${roomId}`);  // Debugging line
//     console.log(`Nickname: ${nickname}`);  // Debugging line

//     if (!roomId) {
//         console.error('Room ID is missing or not defined.');
//         return;
//     }

//     if (!nickname) {
//         console.error('Nickname is missing or not defined.');
//         return;
//     }

//     connectToRoom(roomId);
// });


// connectToRoom(roomId);
// reconnectWebSocket(roomId);
// console.log(`Connected to room ${roomId}`);  // Debugging line