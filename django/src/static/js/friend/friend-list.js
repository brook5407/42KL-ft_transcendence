import { ajax_with_auth } from '../spa/ajax.js';
import { FriendList } from '../spa/components/others/friend-list.js';

export async function renderFriendList() {
	// TODO: call API to get real info
	// const friends = [
	// 	{
	// 		avatar: 'https://via.placeholder.com/150',
	// 		username: 'john_doe',
	// 		nickname: 'John',
	// 	},
	// 	{
	// 		avatar: 'https://via.placeholder.com/150',
	// 		username: 'janedoe',
	// 		nickname: 'Jane',
	// 	},
	// 	{
	// 		avatar: 'https://via.placeholder.com/150',
	// 		username: 'aliceee',
	// 		nickname: 'Alice',
	// 	},
	// ];
	const friends = await ajax_with_auth('/api/friends/', {
		method: 'GET',
	}).then((response) => response.json());

	const friendList = new FriendList({ props: { friends } });
	const friendListElem = document.getElementById('friend-list');
	friendListElem.innerHTML = '';
	friendListElem.appendChild(await friendList.render());
}

renderFriendList();
document.addEventListener('drawer-opened', (e) => {
	if (e.detail.drawerName === 'friend-list') {
		renderFriendList();
	}
});
