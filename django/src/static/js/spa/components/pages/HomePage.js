import { Component } from '../Component.js';
import { Snowfall } from '../../../animation/snow.js';

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
