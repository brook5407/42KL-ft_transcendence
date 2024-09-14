import { getWSHost } from '../websocket.js';
import { showInfoToast } from '../toast.js';

/**
 * @borrows {import('../../../types.js').WSChatMessage}
 */

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

		/** @type {WSChatMessage} */
		const data = JSON.parse(event.data);
		// WXR TODO: add error handling for being blocked or deleted
		// WXR TODO: fix delete friend cannot add back bug
		// WXR TODO: can consider add a notification table for persisting notifications
		// like friend request, friend accepted, friend deleted you, etc.
		if (!data || !data.message || !data.sender || !data.room_id) {
			return;
		}

		if (data.sender.username === window.currentUser.username) {
			return;
		}

		if (
			window.currentDrawer &&
			window.currentDrawer.name === 'chat-room' &&
			window.currentDrawer.room_id === data.room_id
		) {
			window.currentDrawer.appendMessage(data);
		} else if (
			window.currentDrawer &&
			window.currentDrawer.name === 'chat-list'
		) {
			window.currentDrawer.moveChatRoomToTop(data.room_id, data);

			window.playNotificationSound();
		} else {
			this.showToastNotification(data);
			window.playNotificationSound();
		}

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
		if (window.currentDrawer && window.currentDrawer.name === 'chat-room') {
			window.currentDrawer.appendMessage({
				message,
				room_id: roomId,
				sender: {
					username: currentUser.username,
					nickname: currentUser.profile.nickname,
					avatar: currentUser.profile.avatar,
				},
			});
		}
	}

	_dispatchNewMessageEvent(data) {
		const newMessageEvent = new CustomEvent('new-message', {
			detail: JSON.parse(data),
		});
		document.dispatchEvent(newMessageEvent);
	}

	showToastNotification(data) {
		let toOpen = {
			type: 'drawer',
			name: 'chat-room',
			data: {
				url: 'drawer/chat-room',
			},
		};
		if (data.type === 'private_chat_message') {
			toOpen.data.queryParams = {
				username: data.sender.username,
			};
			showInfoToast(
				data.message,
				`${data.sender.nickname}`,
				data.sender.avatar,
				toOpen
			);
		} else {
			toOpen.data.queryParams = {
				room_id: data.room_id,
			};
			showInfoToast(
				`${data.sender.nickname}: ${data.message}`,
				`${data.room_name}`,
				data.cover_image,
				toOpen
			);
		}
	}

	destroy() {
		this.socket.close();
	}
}

document.addEventListener('user-ready', () => {
	window.chatController = new ChatController();
});

document.addEventListener('user-cleared', () => {
	window.chatController.destroy();
	window.chatController = null;
});
