import { FriendRequests } from '../spa/components/others/friend-requests.js';

export async function renderFriendRequests() {
	// call API to get real info
	const friendRequests = [
		{
			avatar: 'https://via.placeholder.com/150',
			nickname: 'John Doe',
			username: 'johndoe',
			status: 'pending',
		},
		{
			avatar: 'https://via.placeholder.com/150',
			nickname: 'Jane Doe',
			username: 'janedoe',
			status: 'accepted',
		},
		{
			avatar: 'https://via.placeholder.com/150',
			nickname: 'Alice',
			username: 'alice',
			status: 'rejected',
		},
	];

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
