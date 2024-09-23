import { getWSHost } from '../websocket.js';
import { showErrorToast, showInfoToast } from '../toast.js';
import { showSuccessMessage } from '../message.js';
import { navigateTo } from '../spa/navigation.js';

const wsHost = getWSHost();

class TournamentController {
	constructor() {
		this.socket = new WebSocket(`${wsHost}/ws/tournament/`);
		this.socket.onopen = this._onOpen.bind(this);
		this.socket.addEventListener('message', this._onMessage.bind(this));
		this.socket.onclose = this._onClose.bind(this);
		this.socket.onerror = this._onError.bind(this);

		this.participantsNicknames = [];

		this.currentTournamentId = null;
		this.isOwner = false;
	}

	setCurrentTournamentId(tournamentId) {
		this.currentTournamentId = tournamentId;
		window.currentUser.active_tournament_id = tournamentId;
	}

	attachTournamentClient(tournamentClient) {
		this.tournamentClient = tournamentClient;
		this.tournamentClientMessageHandler =
			tournamentClient.onMessage.bind(tournamentClient);
		this.tournamentClient.socket = this.socket;
		this.tournamentClient.startTournament(this.participantsNicknames);
	}

	detachTournamentClient() {
		if (!this.tournamentClient) {
			return;
		}
		this.tournamentClient = null;
		this.tournamentClientMessageHandler = null;
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
		/** @type {WSTournamentMessage} */
		const data = JSON.parse(e.data);
		// console.log('Tournament WS message:', data);

		if (data.user_id === window.currentUser.id) {
			console.log('Ignoring own message');
			return;
		}

		switch (data.type) {
			case 'player_joined':
				showInfoToast(data.message);
				this._updateTournamentRoom(data);
				break;
			case 'player_left':
				showInfoToast(data.message);
				this._updateTournamentRoom(data);
				break;
			case 'owner_left':
				showInfoToast(data.message);
				if (window.currentDrawer.name === 'tournament-room') {
					closeDrawer();
				}
				break;
			case 'player_rejoined':
				showInfoToast(data.message);
				this._updateTournamentRoom(data);
				break;
			case 'tournament_started':
				showInfoToast(data.message);
				navigateTo(`/pong/tournament/?tournament_id=${data.tournament_id}`);
				this.participantsNicknames = data.participants_nicknames;
				console.log("Participants' nicknames:", this.participantsNicknames);
				break;
			case 'tournament_ended':
				showInfoToast(data.message);
				this.tournamentClientMessageHandler(e);
				this.reset();
				this.detachTournamentClient();
				break;
			case 'error':
				showErrorToast(data.message);
				break;
			// default:
			// 	console.error('Unknown message type:', data.type);
		}

		if (this.tournamentClientMessageHandler) {
			this.tournamentClientMessageHandler(e);
		}
	}

	/**
	 *
	 * @param {WSTournamentMessage} data
	 */
	async _updateTournamentRoom(data) {
		if (window.currentDrawer.name !== 'tournament-room') {
			return;
		}

		const tournamentMembersContainer = document.querySelector(
			'.tournament-room__members'
		);

		/** @type {TournamentRoom} */
		const tournamentRoom = await this.fetchTournamentRoomDetails(
			data.tournament_id
		);
		if (!tournamentRoom) {
			return;
		}
		console.log(tournamentRoom);

		if (tournamentRoom.status !== 'W') {
			navigateTo(`/pong/tournament/?tournament_id=${data.tournament_id}`);
			return;
		}

		tournamentMembersContainer.innerHTML = `
		${tournamentRoom.players
			.map(
				(player) => `
			<div class="tournament-room__member-avatar">
				<img src="${player.player.user.profile.avatar}" alt="${player.player.user.username} avatar" width="30" height="30" />
			</div>
		`
			)
			.join('')}
		${Array(window.tournamentMaxPlayers - tournamentRoom.players.length)
			.fill(
				'<div class="tournament-room__member-avatar tournament-room__member-empty"><span>+</span></div>'
			)
			.join('')}
		`;

		if (tournamentRoom.owner.id === window.currentUser.id) {
			const startButton = document.querySelector(
				'.tournament-room__start-button'
			);
			if (
				tournamentRoom.players.length >= 4 &&
				tournamentRoom.players.length % 2 === 0
			) {
				startButton.removeAttribute('disabled');
			} else {
				startButton.setAttribute('disabled', '');
			}
		}
	}

	/**
	 *
	 * @param {string} tournamentId
	 * @returns {Promise<TournamentRoom>}
	 */
	async fetchTournamentRoomDetails(tournamentId) {
		try {
			const res = await ajaxWithAuth(
				`/api/tournament-room/${tournamentId}/details/`,
				{
					method: 'GET',
				}
			);
			return res.json();
		} catch (error) {
			console.error(error);
			showErrorToast('Failed to fetch tournament room details');
			return null;
		}
	}

	async joinTournament(tournamentId) {
		if (this.currentTournamentId && this.currentTournamentId !== tournamentId) {
			console.error('Already in a tournament');
			return false;
		}

		if (this.currentTournamentId === tournamentId) {
			const tournamentRoom = await this.fetchTournamentRoomDetails(
				tournamentId
			);
			if (!tournamentRoom) {
				return false;
			}
			console.log('rejoin');
			this.socket.send(
				JSON.stringify({
					type: 'rejoin_tournament',
					tournament_id: tournamentId,
				})
			);
			if (tournamentRoom.owner.id === window.currentUser.id) {
				this.isOwner = true;
			}
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
		ajaxWithAuth(`/api/tournament-room/${this.currentTournamentId}/start/`, {
			method: 'POST',
		}).then((res) => {
			this.socket.send(JSON.stringify({ type: 'start_tournament' }));
		});
	}

	reset() {
		this.setCurrentTournamentId(null);
		this.isOwner = false;
	}

	destroy() {
		this.reset();
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
