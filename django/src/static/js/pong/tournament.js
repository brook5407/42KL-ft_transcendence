import { getWSHost } from '../websocket.js';
import { showErrorToast, showInfoToast } from '../toast.js';
import { showSuccessMessage } from '../message.js';

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

	setCurrentTournamentId(tournamentId) {
		this.currentTournamentId = tournamentId;
		window.currentUser.active_tournament_id = tournamentId;
	}

	_onOpen() {
		console.log('Tournament Websocket connection established');
		if (window.currentUser.active_tournament_id) {
			// if user has active tournament, rejoin
			this.currentTournamentId = window.currentUser.active_tournament_id;
			this.joinTournament(window.currentUser.active_tournament_id);
		}
	}

	_onError(error) {
		console.error('Tournament WebSocket error:', error);
	}

	_onClose(event) {
		console.log('Tournament WebSocket connection closed:');
	}

	_onMessage(e) {
		const data = JSON.parse(e.data);
		console.log(data);

		if (data.user_id === window.currentUser.id) {
			console.log('Ignoring own message');
			return;
		}

		switch (data.type) {
			case 'player_joined':
				showInfoToast('Player joined');
				// WXR TODO: update tournament room UI if needed
				break;
			case 'player_left':
				showInfoToast('Player left');
				// WXR TODO: update tournament room UI if needed
				break;
			case 'owner_left':
				showInfoToast('Owner left');
				// closeDrawer() if on the tournament room drawer
				break;
			case 'player_rejoined':
				showInfoToast('Player rejoined');
				// WXR TODO: update tournament room UI if needed
				break;
			case 'tournament_started':
				showInfoToast('Tournament started');
				break;
			case 'error':
				showErrorToast(data.message);
				break;
			default:
				console.error('Unknown message type:', data.type);
		}
	}

	async joinTournament(tournamentId) {
		if (this.currentTournamentId && this.currentTournamentId !== tournamentId) {
			console.error('Already in a tournament');
			return false;
		}

		if (this.currentTournamentId === tournamentId) {
			console.log('rejoin');
			this.socket.send(
				JSON.stringify({
					type: 'rejoin_tournament',
					tournament_id: tournamentId,
				})
			);
			openDrawer('tournament-room', {
				url: '/drawer/tournament-room/',
				queryParams: { tournament_room_id: tournamentId },
			});
		} else {
			// new join
			console.log('Joining tournament:', tournamentId);
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

			this.socket.send(
				JSON.stringify({
					type: 'join_tournament',
					user_id: window.currentUser.id,
					tournament_id: tournamentId,
				})
			);
		}

		this.setCurrentTournamentId(tournamentId);
		return true;
	}

	leaveTournament() {
		if (!this.currentTournamentId) {
			console.error('No tournament to leave');
			return;
		}
		console.log('Leaving tournament');
		ajaxWithAuth(`/api/tournament-room/${this.currentTournamentId}/leave/`, {
			method: 'POST',
		})
			.then((res) => {
				if (!res.ok) {
					throw 'Failed to leave tournament';
				}
				this.socket.send(
					JSON.stringify({
						type: 'leave_tournament',
						user_id: window.currentUser.id,
						tournament_id: this.currentTournamentId,
					})
				);
			})
			.then(() => {
				closeDrawer();
				this.reset();
				showSuccessMessage('Successfully left tournament');
			})
			.catch((error) => {
				console.error(error);
				showErrorToast('Failed to leave tournament');
			});
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
		const tournamentRoomId = await res.json();
		console.log(tournamentRoomId);
		this.tournamentRoomId = tournamentRoomId;

		this.socket.send(
			JSON.stringify({
				type: 'create_tournament',
				user_id: window.currentUser.id,
				tournament_id: tournamentRoomId,
			})
		);

		return tournamentRoomId;
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
		this.setCurrentTournamentId(null);
		this.isOwner = false;
	}

	destroy() {
		this.socket.close();
	}
}

document.addEventListener('user-ready', () => {
	window.tournamentController = new TournamentController();
});

document.addEventListener('user-cleared', () => {
	window.tournamentController.destroy();
	window.tournamentController = null;
});

window.tournamentMaxPlayers = 8;
