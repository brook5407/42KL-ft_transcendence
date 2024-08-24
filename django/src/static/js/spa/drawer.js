import { DRAWER_CONTAINER } from './components/component.js';
import { Profile } from './components/drawer/profile.js';
import { Settings } from './components/drawer/settings.js';
import { ChatList } from './components/drawer/chat-list.js';
import { ChatRoom } from './components/drawer/chat-room.js';
import { FriendList } from './components/drawer/friend-list.js';
import { FriendRequests } from './components/drawer/friend-requests.js';
import { SearchFriend } from './components/drawer/search-friend.js';

let currentDrawer = null;

export const DRAWERS = {
	profile: Profile,
	settings: Settings,
	'chat-list': ChatList,
	'chat-room': ChatRoom,
	'friend-list': FriendList,
	'friend-requests': FriendRequests,
	'search-friend': SearchFriend,
};

// open drawer buttons handler
document.body.addEventListener('click', (e) => {
	if (e.target.matches('[data-drawer]')) {
		e.preventDefault();
		const drawerName = e.target.getAttribute('data-drawer');
		const drawerUrl = e.target.getAttribute('data-drawer-url') || '';
		openDrawer(drawerName, { url: drawerUrl });
	}
});

// custom event to open drawer
document.addEventListener('open-drawer', (e) => {
	const drawerName = e.detail.drawerName;
	openDrawer(drawerName, e.detail.data);
});

function dispatchDrawerOpenedEvent(e = null) {
	document.dispatchEvent(new CustomEvent('drawer-opened', e));
}

export async function openDrawer(drawerName, data = {}) {
	const drawerClass = DRAWERS[drawerName];
	const drawer = new drawerClass({
		url: data.url,
		state: data.state || {},
	});

	console.log('drawerName:', drawerName);

	if (drawer) {
		currentDrawer = drawer;
		const element = await drawer.render();
		DRAWER_CONTAINER.innerHTML = '';
		DRAWER_CONTAINER.appendChild(element);
		setTimeout(() => {
			activateDrawer();
			dispatchDrawerOpenedEvent({
				detail: { drawerName },
			});
		}, 100);
		return element;
	} else {
		console.error('Drawer not found:', drawerName);
	}
}

export function closeDrawer() {
	const drawerOverlay = document.getElementById('drawerOverlay');
	const drawer = document.getElementById('drawer');
	drawerOverlay.classList.remove('drawer-active');
	drawer.classList.remove('drawer-active');
	setTimeout(() => {
		DRAWER_CONTAINER.innerHTML = '';
		currentDrawer?.destroy();
	}, 500);
}

function activateDrawer() {
	const drawerOverlay = document.getElementById('drawerOverlay');
	const drawer = document.getElementById('drawer');
	drawerOverlay.classList.add('drawer-active');
	drawer.classList.add('drawer-active');

	// document
	// 	.getElementById('closeDrawerBtn')
	// 	.addEventListener('click', closeDrawer);

	document
		.getElementById('drawerOverlay')
		.addEventListener('click', closeDrawer);
}

window.closeDrawer = closeDrawer;
