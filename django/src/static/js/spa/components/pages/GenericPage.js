import { Component } from '../Component.js';

export class GenericPage extends Component {
	constructor(params) {
		super(params);

		this.boundHandlePageLoaded = this.handlePageLoaded.bind(this);
	}

	async handlePageLoaded(e) {}

	async initComponent() {
		document.addEventListener('page-loaded', this.boundHandlePageLoaded);
	}

	// override
	destroy() {
		super.destroy();
		document.removeEventListener('page-loaded', this.boundHandlePageLoaded);
	}

	template() {
		return `
			<div>
				<h1>Page</h1>
			</div>
		`;
	}
}
