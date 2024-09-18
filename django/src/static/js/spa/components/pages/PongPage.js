import { GenericPage } from './GenericPage.js';
import { Snowfall } from '../../../animation/snow.js';
import { GameClient } from '../../../pong/pong.js';
import { MatchMakingManager } from '../../../pong/matchmaking.js';

export class PongPage extends GenericPage {
	constructor(params) {
		super(params);
		if (this.url === '' || this.url === null) {
			this.url = '/pong';
		}
	}

	async handlePageLoaded(e) {
		console.log('page loaded');
		this.gameMode = document.getElementById('game_mode').textContent;
		if (this.gameMode) {
			this.gameMode = JSON.parse(this.gameMode);
		}
		console.log('game mode:', this.gameMode);
		if (this.gameMode === 'pvp') {
			this.startMatchmaking();
		} else {
			this.matchId = document.getElementById('match_id').textContent;
			if (this.matchId) {
				this.matchId = JSON.parse(this.matchId);
			}
			this.startGame(this.matchId);
		}
	}

	async startMatchmaking() {
		this.matchMakingManager = new MatchMakingManager(
			this.gameMode,
			(matchId) => {
				this.gameClient = new GameClient(this.gameMode, matchId);
			}
		);
	}

	async startGame(matchId) {
		this.gameClient = new GameClient(this.gameMode, matchId);
	}

	startComponent() {
		super.startComponent();
		// this.snowfall = new Snowfall();
		// this.snowfall.startSnowfall();
	}

	cleanupComponent() {
		super.cleanupComponent();
		// this.snowfall.stopSnowfall();
		if (this.gameClient) {
			this.gameClient.destroy();
		}
		if (this.matchMakingManager) {
			this.matchMakingManager.destroy();
		}
	}

	template() {
		return `
			<div>
				<h1>Pong page template</h1>
			</div>
		`;
	}
}
