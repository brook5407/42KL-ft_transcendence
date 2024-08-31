import { openDrawer } from '../../drawer.js';
import { Component } from '../component.js';

export class FriendListTile extends Component {
	constructor(params) {
		super(params);

		this.friend = this.props.friend;
	}

	startComponent() {
		this.element
			.querySelector('.friend-list-tile__avatar')
			.addEventListener('click', () => {
				openDrawer('friend-profile', {
					url: `drawer/friend-drawer?username=${this.friend.user.username}`,
				});
			});
		this.element
			.querySelector('.icon-action[title="Chat"]')
			.addEventListener('click', () => {
				// openDrawer('chat'); WXR TODO
			});
	}

	template() {
		if (!this.friend) {
			return '';
		}
		return `
		<div class="friend-list-tile">
			<div class="friend-list-tile__avatar">
				<img src="${this.friend.avatar ?? ''}" alt="avatar" />
			</div>
			<div class="friend-list-tile__info">
				<div class="friend-list-tile__nickname">${
					this.friend.nickname ?? 'Anonymous'
				}</div>
				<div class="friend-list-tile__username">@${this.friend.user.username}</div>
			</div>
			<div class="friend-list-tile__action">
				<a class="icon-action" title="Chat">
					<i class="fa fa-comments"></i>
				</a>
			</div>
		</div>
		`;
	}
}
