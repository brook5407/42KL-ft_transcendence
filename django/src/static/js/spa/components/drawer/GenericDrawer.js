import { Component } from '../Component.js';

export class GenericDrawer extends Component {
	constructor(params) {
		super(params);
	}

	template() {
		return `
			<div>
				<h1>Drawer</h1>
			</div>
		`;
	}
}
