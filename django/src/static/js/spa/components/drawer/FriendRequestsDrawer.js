import { Component } from '../Component.js';
import { FriendRequests } from '../others/FriendRequests.js';

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

	// override
	async initComponent() {
		document.addEventListener(
			'drawer-opened',
			this.boundHandleFriendRequestsDrawerOpened
		);
	}

	// override
	destroy() {
		super.destroy();
		document.removeEventListener(
			'drawer-opened',
			this.boundHandleFriendRequestsDrawerOpened
		);
		this.friendRequestsComponent?.destroy();
	}

	// override
	template() {
		return `
			<div>
				<h1>Drawer</h1>
			</div>
		`;
	}
}
