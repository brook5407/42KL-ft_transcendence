import { Component } from '../Component.js';

export class SignIn extends Component {
	constructor(params) {
		super(params);
	}

	template() {
		return `
			<div>
				<h1>Modal</h1>
			</div>
		`;
	}
}
