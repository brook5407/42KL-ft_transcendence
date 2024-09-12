import { Component } from '../Component.js';
import { Snowfall } from '../../../animation/snow.js';

// const hitSound = new Audio('/static/audio/hit.mp3');
// const scoreSound = new Audio('/static/audio/score.mp3');
// // Preload audio
// hitSound.load();
// scoreSound.load();


export class HomePage extends Component {
	constructor(params) {
		super(params);
		if (this.url === '' || this.url === null) {
			this.url = '/home';
		}
	}

	startComponent() {
		super.startComponent();
		this.snowfall = new Snowfall();
		this.snowfall.startSnowfall();
	}

	cleanupComponent() {
		super.cleanupComponent();
		this.snowfall.stopSnowfall();
	}

	template() {
		return `
			<div class="home">
				<h1>Home</h1>
				<p>Welcome to the home page</p>
			</div>
		`;
	}
}
