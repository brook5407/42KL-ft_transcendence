import { Component } from '../component.js';

export class FriendListTile extends Component {
	constructor(params) {
		super(params);
	}

	template() {
		console.log(this.props);
		return `
		<div class="friend-list-tile">
			<div class="friend-list-tile__avatar">
				<img src="${this.props.friend.avatar ?? ''}" alt="avatar" />
			</div>
			<div class="friend-list-tile__info">
				<div class="friend-list-tile__nickname">${
					this.props.friend.nickname ?? 'Anonymous'
				}</div>
				<div class="friend-list-tile__username">@${
					this.props.friend.user.username
				}</div>
			</div>
		</div>
		`;
	}
}
