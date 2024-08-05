import { Component } from '../component.js';

export class Oauth42 extends Component {
	constructor(params) {
		super(params);
		if (this.url === '' || this.url === null) {
			this.url = '/modal/oauth42-modal';
		}
	}

	template() {
		return `
			<div>
				<h1>Modal</h1>
			</div>
		`;
	}
}
