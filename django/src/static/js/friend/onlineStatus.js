export class FriendsOnlineStatus {
	constructor() {
		this.userId = window.currentUser.id;
		this.username = window.currentUser.username;
		this.socket = new WebSocket(
			`ws://${window.location.host}/ws/online-status/`
		);

		this.socket.onopen = () => {
			console.log('Friends online status socket opened');
		};

		this.socket.onmessage = this.onmessage.bind(this);
		this.socket.onclose = this.onclose.bind(this);
	}

	onmessage(event) {
		const data = JSON.parse(event.data);
		console.log('Friends online status data', data);

		// if (data.initial_status) {
		// 	const friends = document.querySelectorAll('.friend-list__tile');
		// 	friends.forEach((friend) => {
		// 		const friendId = friend.getAttribute('data-user-id');
		// 		if (data.initial_status[friendId]) {
		// 			const onlineStatus = data.initial_status[friendId];
		// 			const statusElem = friend.querySelector('.friend-list__status');
		// 			statusElem.textContent = onlineStatus ? 'Online' : 'Offline';
		// 			statusElem.classList.add(
		// 				onlineStatus
		// 					? 'friend-list__status--online'
		// 					: 'friend-list__status--offline'
		// 			);
		// 		}
		// 	});
		// }
	}

	onclose(event) {
		console.log('Friends online status socket closed');
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
