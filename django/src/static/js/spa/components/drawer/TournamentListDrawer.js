import { GenericDrawer } from './GenericDrawer.js';

/**
 * @borrows {import("../../../types.js").TournamentRoom}
 */

export class TournamentListDrawer extends GenericDrawer {
	constructor(params) {
		super(params);

		this.tournamentRooms = [];

		this.tournamentListContainer = null;

		this.shufflePageSize = 5;
	}

	// override
	async handleDrawerOpened(e) {
		this.tournamentListContainer = document.querySelector('#tournament-list');

		if (!this.tournamentListContainer) {
			return;
		}

		this.shuffleTournamentRooms();
	}

	/**
	 * @returns {Promise<TournamentRoom[]>}
	 */
	async fetchShuffledTournamentRooms() {
		const res = await ajaxWithAuth('/api/tournament-room/shuffle/', {
			method: 'GET',
			params: {
				size: this.shufflePageSize,
			},
		});

		if (!res.ok) {
			return [];
		}

		const data = await res.json();
		console.log(data);

		/** @type {TournamentRoom[]} */
		const tournamentRooms = data.results;

		this.ptournamentRooms = tournamentRooms;
		return tournamentRooms;
	}

	async shuffleTournamentRooms() {
		// WXR TODO: remove previous rooms and display loading effect while fetching
		const tournamentRooms = await this.fetchShuffledTournamentRooms();
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

		// WXR TODO

		return div;
	}
}
