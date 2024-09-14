import { Component } from '../Component.js';

export class GenericDrawer extends Component {
	constructor(params) {
		super(params);

		this.boundHandleDrawerOpened = this.handleDrawerOpened.bind(this);
	}

	async handleDrawerOpened(e) {}

	async initComponent() {
		document.addEventListener('drawer-opened', this.boundHandleDrawerOpened);
	}

	// override
	destroy() {
		super.destroy();
		document.removeEventListener('drawer-opened', this.boundHandleDrawerOpened);
	}

	template() {
		return `
			<div>
				<h1>Drawer</h1>
			</div>
		`;
	}
}
