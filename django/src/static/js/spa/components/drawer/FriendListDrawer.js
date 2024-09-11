import { Component } from '../Component.js';
import { FriendList } from '../others/FriendList.js';

export class FriendListDrawer extends Component {
	constructor(params) {
		super(params);
		this.friendList = null;

		this.boundHandleFriendListDrawerOpened =
			this.handleFriendListDrawerOpened.bind(this);
	}

	async renderFriendList() {
		this.friendList = new FriendList();
		const friendListElem = document.getElementById('friend-list');
		friendListElem.innerHTML = '';
		friendListElem.appendChild(await this.friendList.render());

		const friendRequestsIcon = document.querySelector(
			'.drawer-bottom-right-icon img'
		);
		const pendingFriendRequests = await this.getPendingFriendRequests();
		friendRequestsIcon.addUnreadCount(pendingFriendRequests.length);
	}

	async getPendingFriendRequests() {
		const allFriendRequests = await ajaxWithAuth(
			'/api/friend-requests/to_me/',
			{
				method: 'GET',
			}
		).then((res) => res.json());
		return allFriendRequests.filter((fReq) => fReq.status === 'P');
	}

	handleFriendListDrawerOpened(e) {
		if (e.detail.drawerName === 'friend-list') {
			this.renderFriendList();
		}
	}

	// override
	async initComponent() {
		document.addEventListener(
			'drawer-opened',
			this.boundHandleFriendListDrawerOpened
		);
	}

	// override
	destroy() {
		super.destroy();
		document.removeEventListener(
			'drawer-opened',
			this.boundHandleFriendListDrawerOpened
		);
		this.friendList?.destroy();
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
