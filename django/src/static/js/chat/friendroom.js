import { getWebSocketConfig, getChatConfig } from './chatConfig.js';

window.config = {};

const connections = new Map();
let socket = null;
let socketURL = null;

// Set up event listeners once the drawer is opened
document.addEventListener('drawer-opened', () => {
    // loadMessages(roomId, 1);
    console.log('Drawer opened. Setting up event listeners...');
    updateConfiguration();
    connectToRoom(window.config.roomId);
});

// let currentPage = 1;
// const messagesPerPage = 20;  // Adjust to how many messages per page you want
// let hasNextPage = true;  // Assume there are more messages to load initially
// let isLoading = false;  // To avoid multiple concurrent requests

// // Initial load of the first page of messages when the DOM is ready
// document.addEventListener('drawer-opened', async () => {
//     console.log('Drawer opened. Loading messages...AAAAAAAAAAAA');
//     const roomId = window.config?.roomId;
//     if (!roomId) {
//         console.error('Room ID is missing.');
//         return;
//     }
//     console.log('Load the first page of messages : Room ID:', roomId);
//     // Load the first page of messages
//     await loadMessages(roomId, currentPage);
// });

// document.addEventListener('drawer-closed', () => {
//     if (roomId) {
//         console.log('Disconnecting from all rooms...');
//         disconnectFromRoom(roomId);
//     }
// });

// window.addEventListener('beforeunload', () => {
//     console.log('Disconnecting from all rooms...');
//     disconnectFromRoom(roomId);
// });

// function disconnectFromRoom(roomId) {
//     socket = connections.get(roomId);
//     if (socket) {
//         socket.close();
//         connections.delete(roomId);
//         console.log(`Disconnected from room ${roomId}`);
//     }
// }

function updateConfiguration() {
    const { host, protocol, port } = getWebSocketConfig();
    const { nickname, roomId } = getChatConfig();
    
    if (!roomId || !nickname) {
        console.error('Room ID or nickname is missing.');
        return;
    }
    
    window.config = { host, protocol, port, nickname, roomId };
    socketURL = `${protocol}//${host}:${port}/ws/drawer/chat-friendroom/${roomId}/?customer_name=${nickname}`;
    
    console.log(`Updated socketURL to ${socketURL}`);

    // Reinitialize event listeners to ensure they are correctly attached
    document.getElementById('message-input').addEventListener('keydown', handleMessage);
    document.getElementById('send-button').addEventListener('click', sendMessage);
}

function connectToRoom(roomId) {
    if (!roomId) {
        console.error('Room ID is required to connect.');
        return;
    }
    
    if (connections.has(roomId)) {
        console.log(`Already connected to room ${roomId}`);
        return;
    }

    // Close the existing WebSocket connection if it exists
    if (socket) {
        socket.close();
        socket = null;
    }
    socket = new WebSocket(socketURL);

    socket.onopen = () => handleSocketOpen(roomId);
    socket.onmessage = (event) => handleSocketMessage(event, roomId);
    socket.onclose = () => handleSocketClose(roomId);
    socket.onerror = handleSocketError;

    connections.set(roomId, socket);
    console.log(`Connecting to room ${roomId}`);
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
    // reconnectWebSocket(roomId);
}

function handleSocketError(error) {
    console.error('WebSocket error:', error);
}

function reconnectWebSocket(roomId) {
    let retries = 0;
    const maxRetries = 5;

    function tryReconnect() {
        if (retries >= maxRetries) {
            console.error('Max reconnect attempts reached. Giving up.');
            return;
        }
        retries++;
        console.log(`Reconnecting to room ${roomId}... (Attempt ${retries}/${maxRetries})`);
        updateConfiguration(); // Update the configuration and socketURL
        connectToRoom(roomId); // Reconnect to the room with the new socketURL
    }

    setTimeout(tryReconnect, 3000);
}

function handleMessage(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    const message = document.getElementById('message-input').value.trim();
    if (message && socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            room_id: window.config.roomId,
            type: 'message',
            name: window.config.nickname,
            message: message,
        }));
        document.getElementById('message-input').value = '';
    } else {
        socket_state(socket);
        reconnectWebSocket(window.config.roomId);
    }
}

function displayChatMessage(message, name, roomId) {
    if (typeof message !== 'string') {
        console.error('Invalid input: expected a string.');
        return;
    }

    // const messageContainer = document.querySelector(`.chat-messages[data-room="${roomId}"]`);
    const messageContainer = document.querySelector(`.chat-messages`);
    if (!messageContainer) return;

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

function displayImage(imageUrl, name, roomId) {
    const imageContainer = document.querySelector(`.chat-messages[data-room="${roomId}"]`);
    if (!imageContainer) return;

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





// // Function to fetch chat messages for a specific room
// function fetchMessages(roomId) {
//     fetch(`/chatroom/${roomId}/messages/`)
//         .then(response => response.json())
//         .then(data => {
//             const messagesContainer = document.getElementById('messages-container');
//             messagesContainer.innerHTML = '';  // Clear any existing messages
            
//             data.messages.forEach(message => {
//                 const messageElement = document.createElement('div');
//                 messageElement.classList.add('message');
//                 messageElement.innerHTML = `<strong>${message.sender}</strong> to <strong>${message.receiver}</strong>: ${message.message} <span class="timestamp">(${message.timestamp})</span>`;
//                 messagesContainer.appendChild(messageElement);
//             });
//         })
//         .catch(error => console.error('Error fetching messages:', error));
// }

// // Example usage (assumes you have the room ID from somewhere in your app)
// const roomId = 'your-room-id-here';  // Replace with actual room ID
// fetchMessages(roomId);

//  -----------------------------------------------------------------------------------------------------------------------------








// // Async function to fetch messages from the server using ajaxWithAuth
// async function fetchMessages(roomId) {
//     try {
//         const response = await ajaxWithAuth(`/chatroom/${roomId}/messages/`, {
//             method: 'GET'
//         });

//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }

//         const data = await response.json();
//         return data.messages;
//     } catch (error) {
//         console.error('There was a problem with the fetch operation:', error);
//         return [];
//     }
// }

// // Fetch and display messages once the DOM is ready
// document.addEventListener('DOMContentLoaded', async () => {
//     // const roomId = 'some-room-id';  // Replace this with the actual room ID in your app
//     const messages = await fetchMessages(roomId);

//     const messagesContainer = document.getElementById('messages-container');
//     messagesContainer.innerHTML = '';  // Clear the container before displaying new messages

//     messages.forEach(message => {
//         const messageElement = document.createElement('div');
//         messageElement.textContent = `[${message.timestamp}] ${message.sender} to ${message.receiver}: ${message.message}`;
//         messagesContainer.appendChild(messageElement);
//     });
// });

//  -----------------------------------------------------------------------------------------------------------------------------







// only fetch messages after the drawer is already displayed to the user, use a drawer-opened event listener, and do whatever in that event function
// pagination you refer to DRF documentation, display messages should be the same as your existing code that appends the message to the messages container
// this part shouldn't be hard for you 
// const messages = await fetchMessages(roomId, page=1); // fetch the first page of messages
// displayMessages(messages); // display the messages
// // then you can add a button to fetch more messages, and display them in the same way as above

// // Function to fetch messages from the server
// async function fetchMessages(roomId, page) {
//     try {
//         const response = await fetch(`/chatroom/${roomId}/messages/?page=${page}`);
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         const data = await response.json();
//         return data.messages;
//     } catch (error) {
//         console.error('There was a problem with the fetch operation:', error);
//         return [];
//     }
// }

// // Function to display messages in the DOM
// function displayMessages(messages) {
//     const messagesContainer = document.getElementById('messages-container');
//     messagesContainer.innerHTML = '';  // Clear the container before displaying new messages
//     messages.forEach(message => {
//         const messageElement = document.createElement('div');
//         messageElement.textContent = `[${message.timestamp}] ${message.sender} to ${message.receiver}: ${message.message}`;
//         messagesContainer.appendChild(messageElement);
//     });
// }

//  -----------------------------------------------------------------------------------------------------------------------------

// let currentPage = 1;
// const messagesPerPage = 20;  // Adjust to how many messages per page you want
// let hasNextPage = true;  // Assume there are more messages to load initially
// let isLoading = false;  // To avoid multiple concurrent requests

// Fetch messages for a specific room and page
async function fetchMessages(roomId, page = 1) {
    try {
        // Fetch paginated messages from the backend API
        const response = await ajaxWithAuth(`/chatroom/${roomId}/messages/?page=${page}&per_page=${messagesPerPage}`, {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return { messages: [], has_next: false };
    }
}

// Function to load and display messages for a specific page
async function loadMessages(roomId, page) {
    console.log(`Loading messages for room ${roomId}, page ${page}...`);
    if (isLoading) return;  // Prevent loading multiple times at once
    isLoading = true;

    const { messages, has_next } = await fetchMessages(roomId, page);
    hasNextPage = has_next;

    const messagesContainer = document.querySelector(`.chat-messages[data-room="${roomId}"]`);
    if (!messagesContainer)
    {
        console.error('Messages container not found.');
        isLoading = false;
        return;
    }

    // Store the current scroll height before appending new messages
    const currentScrollHeight = messagesContainer.scrollHeight;

    // Append new messages at the top (for older messages)
    messages.forEach(message => {
        const messageElement = document.createElement('div');
        const receiverText = message.receiver ? `to ${message.receiver}` : 'to everyone';
        messageElement.textContent = `[${message.timestamp}] ${message.sender} ${receiverText}: ${message.message}`;
        console.log("messageElement.textContent: BBBBB", messageElement.textContent);
        messagesContainer.prepend(messageElement);  // Prepend to show older messages at the top
    });

    // Adjust the scroll position so the user stays in the same position after loading new messages
    messagesContainer.scrollTop = messagesContainer.scrollHeight - currentScrollHeight;

    isLoading = false;
}

// Add infinite scroll logic (detect when the user scrolls to the top)
document.getElementById('chat-messages').addEventListener('scroll', async function() {
    // If scrollTop is 0 and there are more pages to load, load the next page
    if (this.scrollTop === 0 && hasNextPage && !isLoading) {
        currentPage++;
        await loadMessages(window.config.roomId, currentPage);
    }
});

// // Initial load of the first page of messages when the DOM is ready
// document.addEventListener('drawer-opened', async () => {
//     console.log('Drawer opened. Loading messages...AAAAAAAAAAAA');
//     const roomId = window.config?.roomId;
//     if (!roomId) {
//         console.error('Room ID is missing.');
//         return;
//     }

//     // Load the first page of messages
//     await loadMessages(roomId, currentPage);
// });

