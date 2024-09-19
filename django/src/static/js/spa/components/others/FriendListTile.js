import { openDrawer } from '../../drawer.js';
import { Component } from '../Component.js';

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
					url: `drawer/friend-drawer`,
					queryParams: {
						username: this.friend.username,
					},
				});
			});
		this.element
			.querySelector('.friend-list-tile__action')
			.addEventListener('click', () => {
				openDrawer('chat-room', {
					url: `drawer/chat-room`,
					queryParams: {
						username: this.friend.username,
					},
					props: {
						is_group_chat: false,
					},
				});
			});

		// show online status
		this.element
			.querySelectorAll('.friend-list-tile__avatar img')
			.forEach((avatar) => {
				if (window.onlineFriendIds.includes(this.friend.id)) {
					avatar.addOnlineStatus();
				}
			});
	}

	template() {
		if (!this.friend) {
			return '';
		}
		return `
		<div class="friend-list-tile" data-user-id="${this.friend.id}">
			<div class="friend-list-tile__avatar">
				<img src="${this.friend.profile.avatar ?? ''}" alt="avatar" />
			</div>
			<div class="friend-list-tile__info">
				<div class="friend-list-tile__nickname">${
					this.friend.profile.nickname ?? 'Anonymous'
				}</div>
				<div class="friend-list-tile__username">@${this.friend.username}</div>
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
