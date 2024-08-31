import { Component } from '../Component.js';
import { FriendListTile } from './FriendListTile.js';
import { FriendsOnlineStatus } from '../../../friend/onlineStatus.js';

export class FriendList extends Component {
	constructor(params) {
		super(params);

		this.friends = [];
		this.filter = '';
		this.friendListTiles = [];

		this.boundUpdate = this.update.bind(this);
		document.addEventListener('friend-requests-update', this.boundUpdate);
	}

	async initComponent() {
		this.friends = await ajaxWithAuth('/api/friends/', {
			method: 'GET',
		}).then((response) => response.json());
	}

	startComponent() {
		this.renderFriendList();
	}

	renderFriendList() {
		const friends = this.friends.filter((friend) => {
			if (this.filter === '') return true;
			return friend.friend.nickname?.includes(this.filter);
		});
		this.friendListTiles = friends.map(
			(friend) => new FriendListTile({ props: { ...friend } })
		);

		const friendListElem = this.element.querySelector('.friend-list__list');
		friendListElem.innerHTML = '';

		async function appendFriendListTile() {
			const friendList = await Promise.all(
				this.friendListTiles.map((friendTile) => friendTile.render())
			);
			const fragment = document.createDocumentFragment();
			friendList.forEach((friend) => {
				fragment.appendChild(friend);
			});
			friendListElem.appendChild(fragment);
		}
		appendFriendListTile.call(this);
	}

	componentMounted() {
		super.componentMounted();
		const searchInput = this.element.querySelector('.search-bar__input');
		searchInput.addEventListener('input', (e) => {
			this.filterFriends(e.target.value);
		});
	}

	filterFriends(filter = '') {
		this.filter = filter;
		this.renderFriendList();
	}

	destroy() {
		super.destroy();
		this.friendListTiles.forEach((friendTile) => friendTile.destroy());
		document.removeEventListener('friend-requests-update', this.boundUpdate);
	}

	template() {
		return `
			<div class="friend-list">
				<div class="search-bar">
					<input 
						type="text" 
						placeholder="Search friends..." 
						class="search-bar__input"
					/>
					<span class="search-bar__icon">&#128269;</span>
				</div>
				<div class="friend-list__list"></div>
			</div>
		`;
	}
}
