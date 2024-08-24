import { Component } from '../component.js';
import { FriendRequestTile } from './friend-request-tile.js';

export class FriendRequests extends Component {
	constructor(params) {
		super(params);

		this.friendReqTiles = [];
	}

	startComponent() {
		this.renderFriendRequests();
	}

	renderFriendRequests() {
		const friendRequests = this.props.friendRequests;
		const friendReqTiles = friendRequests.map((fReq) =>
			new FriendRequestTile({ props: { ...fReq } }).render()
		);
		this.friendReqTiles = friendReqTiles;

		const friendReqElem = this.element.querySelector('.friend-requests__list');
		friendReqElem.innerHTML = '';

		async function appendFriendReqTile() {
			const friendReqs = await Promise.all(friendReqTiles);
			const fragment = document.createDocumentFragment();
			friendReqs.forEach((fReq) => {
				fragment.appendChild(fReq);
			});
			friendReqElem.appendChild(fragment);
		}
		appendFriendReqTile.call(this);
	}

	template() {
		return `
			<div class="friend-requests">
				<div class="friend-requests__list"></div>
			</div>
		`;
	}
}
