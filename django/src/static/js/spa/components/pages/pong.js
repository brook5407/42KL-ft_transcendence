import { Component } from '../component.js';
import { Snowfall } from '../../../animation/snow.js';

export class PongPage extends Component {
	constructor(params) {
		super(params);
		if (this.url === '' || this.url === null) {
			this.url = '/pong';
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
			<div>
				<h1>Pong page template</h1>
			</div>
		`;
	}
}
