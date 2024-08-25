export class FriendRequestsLiveUpdate {
	constructor() {
		this.userId = window.currentUser.id;
		this.username = window.currentUser.username;
		this.socket = new WebSocket(
			`ws://${window.location.host}/ws/friend-requests/`
		);

		this.socket.onopen = () => {
			console.log('Friend requests live update socket opened');
		};

		this.socket.onmessage = this.onmessage.bind(this);
		this.socket.onclose = this.onclose.bind(this);
	}

	onmessage(event) {
		const data = JSON.parse(event.data);
		console.log('Friend requests live update data', data);
		if (data.status === 'P') {
			if (data.receiver !== this.username) return;
			showInfoMessage(
				`You have received a friend request from @${data.sender ?? someone}!`
			);
		} else if (data.status === 'A') {
			if (data.sender !== this.username) return;
			showSuccessMessage(
				`@${data.sender ?? someone} has accepted your friend request!`
			);
		} else if (data.status === 'R') {
			if (data.sender !== this.username) return;
			showErrorMessage(
				`@${data.sender ?? someone} has rejected your friend request!`
			);
		}

		playNotificationSound();
		// dispatch friend-requests-update event
		document.dispatchEvent(new Event('friend-requests-update'));
	}

	onclose(event) {
		console.log('Friend requests live update socket closed', event);
	}

	destroy() {
		this.socket.close();
	}
}

let frUpdateObj = null;

document.addEventListener('user-ready', () => {
	frUpdateObj = new FriendRequestsLiveUpdate();
});

document.addEventListener('user-cleared', () => {
	frUpdateObj.destroy();
});
