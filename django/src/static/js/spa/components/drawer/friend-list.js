import { Component } from '../component.js';
import { FriendList } from '../others/friend-list.js';

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
