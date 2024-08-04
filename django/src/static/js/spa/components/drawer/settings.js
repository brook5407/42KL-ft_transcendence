import { Component } from '../component.js';

export class Settings extends Component {
	constructor(params) {
		super(params);
		if (this.url === '') {
			this.url = '/drawer/settings';
		}
	}

	template() {
		return `
			<div>
				<h1>Drawer</h1>
			</div>
		`;
	}
}
