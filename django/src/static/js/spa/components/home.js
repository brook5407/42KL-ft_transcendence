import { Component } from './component.js';

export class HomePage extends Component {
	constructor(params) {
		super(params);
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
