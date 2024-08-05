import { Component } from '../component.js';

export class SignUp extends Component {
	constructor(params) {
		super(params);
		if (this.url === '' || this.url === null) {
			this.url = '/modal/signup-modal';
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
				<h1>Modal</h1>
			</div>
		`;
	}
}
