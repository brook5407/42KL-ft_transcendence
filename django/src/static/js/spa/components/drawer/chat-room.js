import { ajax_with_auth } from '../../ajax.js';
import { Component } from '../component.js';

export class ChatRoom extends Component {
	constructor(params) {
		super(params);
	}

	initComponent() {
		// fetch messages from server
		// const path = '';
		// ajax_with_auth(path, {
		// 	method: 'GET',
		// })
		// 	.then((response) => response.json())
		// 	.then((data) => {
		// 		console.log('data:', data);
		// 	})
		// 	.catch((error) => {
		// 		console.error('error:', error);
		// 	});
	}

	setState(state, options = { update: true }) {
		if (state.roomId !== this.state.roomId) {
			this.queryParams.room_id = state.roomId;
		}
		super.setState(state, options);
	}

	template() {
		return `
			<div>
				<h1>Drawer</h1>
			</div>
		`;
	}
}
