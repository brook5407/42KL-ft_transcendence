import { ajaxWithAuth } from '../../ajax.js';
import { Component } from '../Component.js';

export class ChatRoomDrawer extends Component {
	constructor(params) {
		super(params);
		this.queryParams = {
			room_id: this.state.roomId,
		};
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
