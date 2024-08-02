import { Component } from '../component.js';

export class PongPage extends Component {
	constructor(params) {
		super(params);
		if (this.url === '') {
			this.url = '/pong';
		}
	}

	initComponent() {
		super.initComponent();
	}

	cleanupComponent() {
		super.cleanupComponent();
	}

	template() {
		return `
			<div>
				<h1>Pong page template</h1>
			</div>
		`;
	}
}
