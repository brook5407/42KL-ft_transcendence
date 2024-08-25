import { openDrawer } from '../../drawer.js';
import { Component } from '../component.js';

export class FriendListTile extends Component {
	constructor(params) {
		super(params);
	}

	startComponent() {
		this.element
			.querySelectorAll('.icon-action[data-username]')
			.forEach((element) => {
				element.addEventListener('click', (e) => {
					const username = e.currentTarget.getAttribute('data-username');
					if (element.title === 'View Profile')
						openDrawer('friend-profile', {
							url: `drawer/friend-drawer?username=${username}`,
						});
					else if (element.title === 'Chat') {
						// openDrawer('chat-room', { username });
					}
				});
			});
	}

	template() {
		const friend = this.props.friend;
		if (!friend) {
			return '';
		}
		return `
		<div class="friend-list-tile">
			<div class="friend-list-tile__avatar">
				<img src="${friend.avatar ?? ''}" alt="avatar" />
			</div>
			<div class="friend-list-tile__info">
				<div class="friend-list-tile__nickname">${friend.nickname ?? 'Anonymous'}</div>
				<div class="friend-list-tile__username">@${friend.user.username}</div>
			</div>
			<div class="friend-list-tile__action">
				<a class="icon-action" title="Chat" data-username=${friend.user.username}>
					<i class="fa fa-comments"></i>
				</a>
				<a class="icon-action" title="View Profile" data-username=${
					friend.user.username
				}>
					<i class="fa fa-user"></i>
				</a>
			</div>
		</div>
		`;
	}
}
