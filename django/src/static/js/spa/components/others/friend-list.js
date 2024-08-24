import { Component } from '../component.js';
import { FriendListTile } from './friend-list-tile.js';

export class FriendList extends Component {
	constructor(params) {
		super(params);

		this.filter = '';
	}

	startComponent() {
		this.renderFriendList();
	}

	renderFriendList() {
		const friends = this.props.friends.filter((friend) => {
			if (this.filter === '') return true;
			return friend.friend.nickname?.includes(this.filter);
		});
		const friendListTiles = friends.map((friend) =>
			new FriendListTile({ props: { ...friend } }).render()
		);

		const friendListElem = this.element.querySelector('.friend-list__list');
		friendListElem.innerHTML = '';

		async function appendFriendListTile() {
			const friendList = await Promise.all(friendListTiles);
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
