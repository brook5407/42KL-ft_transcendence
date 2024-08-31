import { Component } from '../component.js';
import { FriendRequests } from '../others/friend-requests.js';

export class FriendRequestsDrawer extends Component {
	constructor(params) {
		super(params);
		this.friendRequestsComponent = null;

		this.boundHandleFriendRequestsDrawerOpened =
			this.handleFriendRequestsDrawerOpened.bind(this);
	}

	async renderFriendRequests() {
		this.friendRequestsComponent = new FriendRequests();
		const friendRequestsElem = document.getElementById('friend-requests');
		friendRequestsElem.innerHTML = '';
		friendRequestsElem.appendChild(await this.friendRequestsComponent.render());
	}

	handleFriendRequestsDrawerOpened(e) {
		if (e.detail.drawerName === 'friend-requests') {
			this.renderFriendRequests();
		}
	}

	async initComponent() {
		document.addEventListener(
			'drawer-opened',
			this.boundHandleFriendRequestsDrawerOpened
		);
	}

	destroy() {
		super.destroy();
		document.removeEventListener(
			'drawer-opened',
			this.boundHandleFriendRequestsDrawerOpened
		);
		this.friendRequestsComponent?.destroy();
	}

	template() {
		return `
			<div>
				<h1>Drawer</h1>
			</div>
		`;
	}
}
