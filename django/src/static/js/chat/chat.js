import { getWSHost } from '../websocket.js';
import { showErrorToast, showInfoToast } from '../toast.js';

/**
 * @borrows {import('../types.js').WSChatMessage}
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
		if (data.error) {
			switch (data.error) {
				case 'user_not_found':
					showErrorToast('User not found');
					break;
				case 'not_friend':
					showErrorToast('You are not friend with this user');
					break;
				case 'blocked':
					showErrorToast('You have blocked this friend');
					break;
				case 'blocked_by_other':
					showErrorToast('You are blocked by this friend');
					break;
				default:
					break;
			}
			return;
		}
		if (!data || !data.message || !data.sender || !data.room_id) {
			return;
		}

		// no need to act to own messages
		// if (data.sender.username === window.currentUser.username) {
		// 	return;
		// }

		if (
			window.currentDrawer &&
			window.currentDrawer.name === 'chat-room' &&
			window.currentDrawer.room_id === data.room_id
		) {
			// if currently in the chat room, append the message
			window.currentDrawer.appendMessage(data);
		} else if (
			window.currentDrawer &&
			window.currentDrawer.name === 'chat-list'
		) {
			// if currently in the chat list, move the chat room to the top
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
		// if (window.currentDrawer && window.currentDrawer.name === 'chat-room') {
		// 	window.currentDrawer.appendMessage({
		// 		message,
		// 		room_id: roomId,
		// 		sender: {
		// 			username: currentUser.username,
		// 			nickname: currentUser.profile.nickname,
		// 			avatar: currentUser.profile.avatar,
		// 		},
		// 	});
		// }
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
