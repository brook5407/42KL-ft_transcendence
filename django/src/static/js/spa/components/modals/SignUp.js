import { Component } from '../Component.js';

export class SignUp extends Component {
	constructor(params) {
		super(params);
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
