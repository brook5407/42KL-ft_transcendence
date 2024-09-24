import { getWSHost } from '../websocket.js';

const wsHost = getWSHost();

export class FriendsOnlineStatus {
	constructor() {
		this.userId = window.currentUser.id;
		this.username = window.currentUser.username;
		this.socket = new WebSocket(`${wsHost}/ws/online-status/`);

		this.socket.onopen = () => {
			// console.log('Friends online status socket opened');
		};

		this.socket.onmessage = this.onmessage.bind(this);
		this.socket.onclose = this.onclose.bind(this);
	}

	onmessage(event) {
		const data = JSON.parse(event.data);
		// console.log('Friends online status data', data);

		if (data.online_friend_ids) {
			// the initial online friend list
			window.onlineFriendIds = data.online_friend_ids;
			return;
		}

		// toggle the online status of the friend
		const friendTile = document.querySelector(
			`.friend-list-tile[data-user-id="${data.user_id}"]`
		);
		const avatar = friendTile?.querySelector('.friend-list-tile__avatar img');
		if (data.status === true) {
			// friend online
			window.onlineFriendIds.push(data.user_id);
			if (avatar) {
				avatar.addOnlineStatus();
			}
		} else {
			// friend offline
			const index = window.onlineFriendIds.indexOf(data.user_id);
			if (index > -1) {
				window.onlineFriendIds.splice(index, 1);
			}

			if (avatar) {
				avatar.removeOnlineStatus();
			}
		}
	}

	onclose(event) {
		// console.log('Friends online status socket closed');
	}

	destroy() {
		this.socket.close();
	}
}

let onlineStatusObj = null;

document.addEventListener('user-ready', () => {
	onlineStatusObj = new FriendsOnlineStatus();
});

document.addEventListener('user-cleared', () => {
	onlineStatusObj.destroy();
});
