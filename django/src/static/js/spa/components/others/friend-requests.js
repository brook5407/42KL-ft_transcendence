import { Component } from '../component.js';
import { FriendRequestTile } from './friend-request-tile.js';

export class FriendRequests extends Component {
	constructor(params) {
		super(params);

		this.friendRequests = [];
		this.friendReqTiles = [];

		this.updateEventListener = document.addEventListener(
			'friend-requests-update',
			async () => {
				await this.update();
			}
		);
	}

	async initComponent() {
		this.friendRequests = await ajax_with_auth('/api/friend-requests/to_me/', {
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
		document.removeEventListener(this.updateEventListener);
	}

	template() {
		return `
			<div class="friend-requests">
				<div class="friend-requests__list"></div>
			</div>
		`;
	}
}
