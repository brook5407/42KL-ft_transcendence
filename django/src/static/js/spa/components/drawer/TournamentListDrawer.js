import { GenericDrawer } from './GenericDrawer.js';

/**
 * @borrows {import("../../../types.js").TournamentRoom}
 */

export class TournamentListDrawer extends GenericDrawer {
	constructor(params) {
		super(params);

		this.tournamentRooms = [];

		this.tournamentListContainer = null;

		this.tournamentMaxPlayers = 8;
	}

	// override
	async handleDrawerOpened(e) {
		this.tournamentListContainer = document.querySelector('#tournament-list');

		if (!this.tournamentListContainer) {
			return;
		}

		this.shuffleTournamentRooms();

		document
			.querySelector('#tournament__shuffle-rooms')
			?.addEventListener('click', () => {
				this.shuffleTournamentRooms();
			});
	}

	/**
	 * @returns {Promise<TournamentRoom[]>}
	 */
	async fetchShuffledTournamentRooms() {
		const res = await ajaxWithAuth('/api/tournament-room/shuffle/', {
			method: 'GET',
		});

		if (!res.ok) {
			return [];
		}

		const data = await res.json();
		console.log(data);

		/** @type {TournamentRoom[]} */
		const tournamentRooms = data;

		this.tournamentRooms = tournamentRooms;
		return tournamentRooms;
	}

	async shuffleTournamentRooms() {
		this.tournamentListContainer.innerHTML = '';

		this.tournamentListContainer.innerHTML = '<div>Loading...</div>';
		const tournamentRooms = await this.fetchShuffledTournamentRooms();
		console.log(tournamentRooms);
		this.tournamentListContainer.innerHTML = '';

		this.appendTournamentRooms(tournamentRooms);
	}

	/**
	 *
	 * @param {TournamentRoom[]} tournamentRooms
	 */
	appendTournamentRooms(tournamentRooms) {
		tournamentRooms.forEach((tournamentRoom) => {
			const tournamentRoomElement = this.createChatRoomElement(tournamentRoom);
			this.tournamentListContainer?.appendChild(tournamentRoomElement);
		});
	}

	/**
	 *
	 * @param {TournamentRoom} tournamentRoom
	 * @returns {HTMLDivElement}
	 */
	createChatRoomElement(tournamentRoom) {
		const div = document.createElement('div');
		div.className = 'tournament__room-item';
		div.dataset.roomId = tournamentRoom.id;
		div.innerHTML = `
			<div class="tournament__room-owner-avatar">
				<img src="${tournamentRoom.owner.profile.avatar}" alt="${
			tournamentRoom.owner.username
		} avatar" width="50" height="50" />
			</div>
			<div class="tournament__room-details">
				<div class="tournament__room-name">${tournamentRoom.name}</div>
				<div class="tournament__room-description">${tournamentRoom.description}</div>
				<div class="tournament__room-members">
					${tournamentRoom.players
						.map(
							(player) => `
						<div class="tournament__member-avatar">
							<img src="${player.player.user.profile.avatar}" alt="${player.player.user.username} avatar" width="30" height="30" />
						</div>
					`
						)
						.join('')}
					${Array(this.tournamentMaxPlayers - tournamentRoom.players.length)
						.fill(
							'<div class="tournament__member-avatar tournament__member-empty"><span>+</span></div>'
						)
						.join('')}
				</div>
			</div>
			<div class="tournament__join-button">Join</div>
		`;

		// Add event listener for the join button
		div
			.querySelector('.tournament__join-button')
			.addEventListener('click', () => {
				this.joinTournamentRoom(tournamentRoom.id);
			});
		return div;
	}

	/**
	 * Function to handle joining a tournament room
	 * @param {string} roomId
	 */
	joinTournamentRoom(roomId) {
		window.tournamentController.joinTournament(roomId).then((res) => {
			if (!res) {
				this.shuffleTournamentRooms();
			} else {
				// WXR TODO: open tournament room drawer
			}
		});
	}
}
