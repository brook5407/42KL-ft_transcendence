/**
 * if in chat list drawer
 * 		any new incoming message should change the last message in a chat room tile if necessary
 * if in chat room drawer
 * 		any new incoming message should append to the chat room
 */

import { getWSHost } from '../websocket.js';

const wsHost = getWSHost();

class ChatController {
	constructor() {
		this.socket = new WebSocket(`${wsHost}/ws/chat/`);
		this.socket.onopen = this._onOpen.bind(this);
		this.socket.onmessage = this._onMessage.bind(this);
		this.socket.onclose = this._onClose.bind(this);
		this.socket.onerror = this._onError.bind(this);
	}

	_onOpen() {
		console.log('Chat socket opened');
	}

	_onMessage(event) {
		console.log('Chat socket message:', event.data);

		// WXR TODO: toast notification
		// WXR TODO: play notification sound

		this._dispatchNewMessageEvent(event.data);
	}

	_onClose() {
		console.log('Chat socket closed');
	}

	_onError() {
		console.log('Chat socket error');
	}

	async sendMessage(message, roomId) {
		await ajaxWithAuth(`/api/chat/${roomId}/send/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ message }),
		});
	}

	_dispatchNewMessageEvent(data) {
		const newMessageEvent = new CustomEvent('new-message', {
			detail: JSON.parse(data),
		});
		document.dispatchEvent(newMessageEvent);
	}

	destroy() {
		this.socket.close();
	}
}

document.addEventListener('user-ready', () => {
	window.chat = new ChatController();
});

document.addEventListener('user-cleared', () => {
	window.chat.destroy();
});
