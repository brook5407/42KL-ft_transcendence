import { ajax_with_auth } from '../spa/ajax.js';
import { FriendRequests } from '../spa/components/others/friend-requests.js';

export async function renderFriendRequests() {
	const friendRequests = await ajax_with_auth('/api/friend-requests/to_me/', {
		method: 'GET',
	}).then((res) => res.json());

	console.log(friendRequests);

	const friendRequestsComponent = new FriendRequests({
		props: { friendRequests },
	});
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
