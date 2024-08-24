import { ajax_with_auth } from '../spa/ajax.js';
import { FriendList } from '../spa/components/others/friend-list.js';

export async function renderFriendList() {
	const friends = await ajax_with_auth('/api/friends/', {
		method: 'GET',
	}).then((response) => response.json());

	console.log(friends);

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
