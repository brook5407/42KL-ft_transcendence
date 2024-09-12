import { Component } from '../Component.js';
import { FriendRequestTile } from './FriendRequestTile.js';

export class FriendRequests extends Component {
	constructor(params) {
		super(params);

		this.friendRequests = [];
		this.friendReqTiles = [];

		this.boundUpdate = this.update.bind(this);
		document.addEventListener('friend-requests-update', this.boundUpdate);
	}

	async initComponent() {
		this.friendRequests = await ajaxWithAuth('/api/friend-requests/to_me/', {
			method: 'GET',
		}).then((res) => res.json());
	}

	startComponent() {
		this.renderFriendRequests();
	}

	renderFriendRequests() {
		const friendRequests = this.friendRequests;
		this.friendReqTiles = friendRequests.map(
			(fReq) => new FriendRequestTile({ props: { ...fReq } })
		);

		const friendReqElem = this.element.querySelector('.friend-requests__list');
		friendReqElem.innerHTML = '';

		async function appendFriendReqTile() {
			const friendReqs = await Promise.all(
				this.friendReqTiles.map((fReqTile) => fReqTile.render())
			);
			const fragment = document.createDocumentFragment();
			friendReqs.forEach((fReq) => {
				fragment.appendChild(fReq);
			});
			friendReqElem.appendChild(fragment);
		}
		appendFriendReqTile.call(this);
	}

	destroy() {
		super.destroy();
		this.friendReqTiles.forEach((fReqTile) => fReqTile.destroy());
		document.removeEventListener('friend-requests-update', this.boundUpdate);
	}

	template() {
		return `
			<div class="friend-requests">
				<div class="friend-requests__list"></div>
			</div>
		`;
	}
}
