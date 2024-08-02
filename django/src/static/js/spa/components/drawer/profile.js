import { Component } from '../component.js';

export class Profile extends Component {
	constructor(params) {
		super(params);
		if (this.url === '') {
			this.url = '/drawer/profile';
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
				<h1>Drawer</h1>
			</div>
		`;
	}
}
