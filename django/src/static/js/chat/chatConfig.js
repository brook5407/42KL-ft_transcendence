// // config.js
// function getWebSocketConfig() {
//     let host = window.location.hostname;
//     let protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
//     let port = window.location.port || (protocol === 'wss:' ? '443' : '80');
//     return { host, protocol, port };
// }

// function getChatConfig() {
//     let appConfigElement = document.getElementById('chat-config');
//     return {
//         nickname: appConfigElement.getAttribute('data-nickname'),
//         roomId: appConfigElement.getAttribute('data-room'),
//         appConfigElement: appConfigElement,
//     };
// }

// export var{ host, protocol, port } = getWebSocketConfig();
// export var{ nickname, roomId, appConfigElement } = getChatConfig();

// // window.getWebSocketConfig = getWebSocketConfig;
// // window.getChatConfig = getChatConfig;


// config.js

// Function to get WebSocket configuration
export function getWebSocketConfig() {
    var host = window.location.hostname;
    var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    var port = window.location.port || (protocol === 'wss:' ? '443' : '80');
    return { host, protocol, port };
}

// Function to get Chat configuration
export function getChatConfig() {
    var appConfigElement = document.getElementById('chat-config');
    if (!appConfigElement) {
        console.error('Chat config element not found');
        return { nickname: '', roomId: '', appConfigElement: null };
    }
    return {
        nickname: appConfigElement.getAttribute('data-nickname'),
        roomId: appConfigElement.getAttribute('data-room'),
        appConfigElement: appConfigElement,
    };
}
