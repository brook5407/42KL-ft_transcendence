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
		console.log('Rendering friend list');
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

	async initComponent() {
		document.addEventListener(
			'drawer-opened',
			this.boundHandleFriendListDrawerOpened
		);
	}

	destroy() {
		super.destroy();
		document.removeEventListener(
			'drawer-opened',
			this.boundHandleFriendListDrawerOpened
		);
		this.friendList?.destroy();
	}

	template() {
		return `
			<div>
				<h1>Drawer</h1>
			</div>
		`;
	}
}
