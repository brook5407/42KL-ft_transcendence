import { ajax_with_auth } from '../spa/ajax.js';
import { FriendRequests } from '../spa/components/others/friend-requests.js';

export async function renderFriendRequests() {
	const friendRequestsComponent = new FriendRequests();
	const friendRequestsElem = document.getElementById('friend-requests');
	friendRequestsElem.innerHTML = '';
	friendRequestsElem.appendChild(await friendRequestsComponent.render());
}

renderFriendRequests();
document.addEventListener('drawer-opened', (e) => {
	if (e.detail.drawerName === 'friend-requests') {
		renderFriendRequests();
	}
});
