import { GenericDrawer } from './GenericDrawer.js';

/**
 * @borrows {import("../../../types.js").TournamentRoom}
 */

export class TournamentRoomDrawer extends GenericDrawer {
	constructor(params) {
		super(params);

		this.tournamentRoomContainer = null;
		this.tournamentRoomId = this.queryParams.tournament_room_id;
		this.tournamentMaxPlayers = 8;
	}

	// override
	async handleDrawerOpened(e) {
		this.tournamentRoomContainer = document.querySelector('#tournament-room');

		if (!this.tournamentRoomContainer) {
			return;
		}

		const tournamentRoom = await this.fetchTournamentRoom();
		const tournamentRoomElement = this.createTournamentRoom(tournamentRoom);
		this.tournamentRoomContainer.appendChild(tournamentRoomElement);
	}

	createTournamentRoom(tournamentRoom) {
		const div = document.createElement('div');
		div.classList.add('tournament-room');
		div.innerHTML = `
			<div class="tournament-room__owner-avatar">
				<img src="${tournamentRoom.owner.profile.avatar}" alt="${
			tournamentRoom.owner.username
		} avatar" width="50" height="50" />
			</div>
			<div class="tournament-room__details">
				<div class="tournament-room__name">${tournamentRoom.name}</div>
				<div class="tournament-room__description">${tournamentRoom.description}</div>
				<div class="tournament-room__members">
					${tournamentRoom.players
						.map(
							(player) => `
						<div class="tournament-room__member-avatar">
							<img src="${player.player.user.profile.avatar}" alt="${player.player.user.username} avatar" width="30" height="30" />
						</div>
					`
						)
						.join('')}
					${Array(this.tournamentMaxPlayers - tournamentRoom.players.length)
						.fill(
							'<div class="tournament-room__member-avatar tournament-room__member-empty"><span>+</span></div>'
						)
						.join('')}
				</div>
			</div>
			<div class="tournament-room__actions">
				${
					tournamentRoom.owner.id === window.currentUser.id
						? `
					<button class="tournament-room__start-button" ${
						tournamentRoom.players.length < 4 ||
						tournamentRoom.players.length % 2 !== 0
							? 'disabled'
							: ''
					}>Start</button>
				`
						: ''
				}
				<button class="tournament-room__leave-button">Leave</button>
			</div>
		`;

		const leaveButton = div.querySelector('.tournament-room__leave-button');

		if (tournamentRoom.owner.id === window.currentUser.id) {
			const startButton = div.querySelector('.tournament-room__start-button');
			startButton.addEventListener('click', function () {
				ajaxWithAuth('WXR TODO', {
					method: 'POST',
				});
			});
		}

		leaveButton.addEventListener('click', function () {
			ajaxWithAuth(`/api/tournament-room/${tournamentRoom.id}/leave/`, {
				method: 'POST',
			}).then(() => {
				closeDrawer();
			});
		});

		return div;
	}
}
