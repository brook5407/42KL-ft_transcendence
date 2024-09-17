import { getWSHost } from '../websocket.js';
import { showErrorToast, showInfoToast } from '../toast.js';

const wsHost = getWSHost();

class TournamentController {
	constructor() {
		this.socket = new WebSocket(`${wsHost}/ws/tournament/`);
		this.socket.onopen = this._onOpen.bind(this);
		this.socket.onmessage = this._onMessage.bind(this);
		this.socket.onclose = this._onClose.bind(this);
		this.socket.onerror = this._onError.bind(this);

		this.currentTournamentId = null;
		this.isOwner = false;
	}

	_onOpen() {
		console.log('Tournament Websocket connection established');
	}

	_onError(error) {
		console.error('Tournament WebSocket error:', error);
	}

	_onClose(event) {
		console.log('Tournament WebSocket connection closed:', event);
	}

	_onMessage(e) {
		const data = JSON.parse(e.data);
		console.log(data);

		// WXR TODO: handle rejoin tournament
	}

	async joinTournament(tournamentId) {
		if (this.currentTournamentId) {
			console.error('Already in a tournament');
			return false;
		}

		const res = await ajaxWithAuth(
			`/api/tournament-room/${tournamentId}/join/`,
			{
				method: 'POST',
			}
		);
		if (!res.ok) {
			const error = await res.json();
			console.log(error);
			showErrorToast('Failed to join tournament');
			return false;
		}

		this.currentTournamentId = tournamentId;
		console.log('Joining tournament:', tournamentId);
		this.socket.send(
			JSON.stringify({ type: 'join_tournament', tournament_id: tournamentId })
		);
		return true;
	}

	leaveTournament() {
		if (!this.currentTournamentId) {
			console.error('No tournament to leave');
			return;
		}
		// should not need to call leave tournament API, cuz there can be unexpected disconnections
		console.log('Leaving tournament');
		this.socket.send(JSON.stringify({ type: 'leave_tournament' }));
		this.reset();
	}

	async createTournament(name, description) {
		this.isOwner = true;
		console.log('Creating tournament');
		const res = await ajaxWithAuth('/api/tournament-room/', {
			method: 'POST',
			body: JSON.stringify({
				name,
				description,
			}),
			headers: {
				'Content-Type': 'application/json',
			},
		});
		const tournamentRoomId = await res.text();
		console.log(tournamentRoomId);
		this.tournamentRoomId = tournamentRoomId;
		// this.socket.send(JSON.stringify({ type: 'create_tournament' }));
	}

	startTournament() {
		if (!this.isOwner) {
			console.error('Not the owner of the tournament');
			return;
		}
		console.log('Starting tournament');
		this.socket.send(JSON.stringify({ type: 'start_tournament' }));
	}

	reset() {
		this.currentTournamentId = null;
		this.isOwner = false;
	}

	destroy() {
		this.socket.close();
	}
}

document.addEventListener('user-ready', () => {
	window.tournamentController = new TournamentController();
	if (window.currentUser.active_tournament_id) {
		// WXR TODO: Rejoin the tournament
		window.tournamentController.tour;
	}
});

document.addEventListener('user-cleared', () => {
	window.tournamentController.destroy();
	window.tournamentController = null;
});
