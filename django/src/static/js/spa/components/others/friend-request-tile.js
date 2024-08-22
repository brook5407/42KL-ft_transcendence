import { Component } from '../component.js';

export class FriendRequestTile extends Component {
	constructor(params) {
		super(params);
	}

	template() {
		const status = this.props.status;
		let actionsHTML = '';
		if (status == 'pending') {
			actionsHTML = `
				<div class="friend-request-tile__actions">
					<button class="friend-request-tile__accept">
						<i class="fa fa-check"></i>
					</button>
					<button class="friend-request-tile__reject">
						<i class="fa fa-times"></i>
					</button>
				</div>
			`;
		} else if (status == 'rejected') {
			actionsHTML = `
				<div class="friend-request-tile__rejected-badge">Rejected</div>
			`;
		} else if (status == 'accepted') {
			actionsHTML = `
				<div class="friend-request-tile__accepted-badge">Accepted</div>
			`;
		}

		return `
		<div class="friend-request-tile">
			<div class="friend-request-tile__avatar">
				<img src="${this.props.avatar}" alt="avatar" />
			</div>
			<div class="friend-request-tile__info">
				<div class="friend-request-tile__nickname">${
					this.props.nickname ?? 'Anonymous'
				}</div>
				<div class="friend-request-tile__username">@${this.props.username}</div>
			</div>
			${actionsHTML}
		</div>
		`;
	}
}
