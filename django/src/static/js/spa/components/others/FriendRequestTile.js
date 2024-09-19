import { Component } from '../Component.js';

export class FriendRequestTile extends Component {
	constructor(params) {
		super(params);
	}

	startComponent() {
		if (this.props.status !== 'P') {
			return;
		}
		this.element
			.querySelectorAll(
				'.friend-request-tile__accept, .friend-request-tile__reject'
			)
			.forEach((button) => {
				button.addEventListener('click', async (e) => {
					const friendId = e.currentTarget.value;
					if (button.classList.contains('friend-request-tile__accept')) {
						await this.acceptFriendRequest(friendId);
					} else if (button.classList.contains('friend-request-tile__reject')) {
						await this.rejectFriendRequest(friendId);
					}
				});
			});
	}

	async acceptFriendRequest(friendId) {
		const response = await ajaxWithAuth(
			`/api/friend-requests/${friendId}/accept/`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
			}
		);
		if (response.ok) {
			this.props.status = 'A';
			this.render();
		}
	}

	async rejectFriendRequest(friendId) {
		const response = await ajaxWithAuth(
			`/api/friend-requests/${friendId}/reject/`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
			}
		);
		if (response.ok) {
			this.props.status = 'R';
			this.render();
		}
	}

	template() {
		const status = this.props.status;
		const sender = this.props.sender;
		if (!sender) {
			return '';
		}

		let actionsHTML = '';
		if (status == 'P') {
			actionsHTML = `
				<div class="friend-request-tile__actions">
					<button class="friend-request-tile__accept" value='${this.props.id}'>
						<i class="fa fa-check"></i>
					</button>
					<button class="friend-request-tile__reject" value='${this.props.id}'>
						<i class="fa fa-times"></i>
					</button>
				</div>
			`;
		} else if (status == 'R') {
			actionsHTML = `
				<div class="friend-request-tile__rejected-badge">Rejected</div>
			`;
		} else if (status == 'A') {
			actionsHTML = `
				<div class="friend-request-tile__accepted-badge">Accepted</div>
			`;
		}

		return `
		<div class="friend-request-tile">
			<div class="friend-request-tile__avatar">
				<img src="${sender.profile.avatar ?? ''}" alt="avatar" />
			</div>
			<div class="friend-request-tile__info">
				<div class="friend-request-tile__nickname">${
					sender.profile.nickname ?? 'Anonymous'
				}</div>
				<div class="friend-request-tile__username">@${
					sender?.username ?? 'anonymous'
				}</div>
			</div>
			${actionsHTML}
		</div>
		`;
	}
}
