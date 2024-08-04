import { Component } from '../component.js';

export class ChatList extends Component {
	constructor(params) {
		super(params);
		if (this.url === '') {
			this.url = '/drawer/chat-list';
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
