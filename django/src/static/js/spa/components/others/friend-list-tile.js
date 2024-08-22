import { Component } from '../component.js';

export class FriendListTile extends Component {
	constructor(params) {
		super(params);
	}

	template() {
		return `
		<div class="friend-list-tile">
			<div class="friend-list-tile__avatar">
				<img src="${this.props.avatar}" alt="avatar" />
			</div>
			<div class="friend-list-tile__info">
				<div class="friend-list-tile__nickname">${
					this.props.nickname ?? 'Anonymous'
				}</div>
				<div class="friend-list-tile__username">@${this.props.username}</div>
			</div>
		</div>
		`;
	}
}
