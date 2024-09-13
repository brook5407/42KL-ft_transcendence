/**
 * if in chat list drawer
 * 		any new incoming message should change the last message in a chat room tile if necessary
 * if in chat room drawer
 * 		any new incoming message should append to the chat room
 */

import { getWSHost } from '../websocket.js';
import { showInfoToast } from '../toast.js';

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
		const data = JSON.parse(event.data);
		if (!data || !data.message || !data.sender || !data.room_id) {
			return;
		}

		let toOpen = {
			type: 'drawer',
			name: 'chat-room',
			data: {
				url: 'drawer/chat-room',
			},
		};
		if (data.type === 'private_chat_message') {
			toOpen.data.queryParams = {
				username: data.sender,
			};
		} else {
			toOpen.data.queryParams = {
				room_id: data.room_id,
			};
		}

		// show toast
		showInfoToast(data.message, `New message from ${data.sender}`, toOpen);

		// play notification sound
		window.playNotificationSound();

		// WXR TODO: chat UI update

		this._dispatchNewMessageEvent(event.data);
	}

	_onClose() {
		console.log('Chat socket closed');
	}

	_onError() {
		console.log('Chat socket error');
	}

	async sendMessage(message, roomId) {
		this.socket.send(
			JSON.stringify({
				message,
				room_id: roomId,
			})
		);
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
