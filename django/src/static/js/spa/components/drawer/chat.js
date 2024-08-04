import { Component } from '../component.js';

export class Chat extends Component {
	constructor(params) {
		super(params);
		if (this.url === '') {
			this.url = '/chat/chat-list';
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
