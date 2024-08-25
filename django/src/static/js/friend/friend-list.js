import { FriendList } from '../spa/components/others/friend-list.js';

let friendList = null;

export async function renderFriendList() {
	friendList = new FriendList();
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
