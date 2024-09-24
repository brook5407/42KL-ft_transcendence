import { getWSHost } from '../websocket.js';

const wsHost = getWSHost();

export class MatchMakingManager {
	constructor(gameMode, startMatchCallback = null) {
		this.gameMode = gameMode;
		this.startMatchCallback = startMatchCallback;

		this.socket = new WebSocket(`${wsHost}/ws/matchmaking/`);
		this.socket.onopen = this.onOpen.bind(this);
		this.socket.onerror = this.onError.bind(this);
		this.socket.onclose = this.onClose.bind(this);
		this.socket.onmessage = this.onMessage.bind(this);
	}

	onOpen() {
		// console.log('Matchmaking WebSocket connection established');
	}

	onError(error) {
		console.error('Matchmaking WebSocket error:', error);
	}

	onClose(event) {
		// console.log('Matchmaking WebSocket connection closed:', event);
	}

	onMessage(event) {
		const data = JSON.parse(event.data);
		// console.log(data);

		switch (data.type) {
			case 'start_match':
				this.startMatch(data.match_id);
				break;
			default:
				console.error('Unknown message type:', data.type);
		}
	}

	startMatch(matchId) {
		// console.log(`Match started with ID: ${matchId}`);
		if (this.startMatchCallback) {
			this.startMatchCallback(matchId);
		}
		this.socket.close();
	}

	leaveQueue() {
		this.socket.close();
	}

	destroy() {
		this.socket.close();
	}
}
