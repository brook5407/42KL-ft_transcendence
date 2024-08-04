import { DRAWER_CONTAINER } from './components/component.js';
import { Profile } from './components/drawer/profile.js';
import { Settings } from './components/drawer/settings.js';
import { ChatList } from './components/drawer/chat-list.js';
import { ChatRoom } from './components/drawer/chat-room.js';

export const DRAWERS = {
	profile: new Profile({ url: '/drawer/profile' }),
	settings: new Settings({ url: '/drawer/settings' }),
	'chat-list': new ChatList({ url: '/drawer/chat-list' }),
	'chat-room': new ChatRoom({
		url: '/drawer/chat-room',
		state: { roomId: null },
	}),
};

// open drawer buttons handler
document.body.addEventListener('click', (e) => {
	if (e.target.matches('[data-drawer]')) {
		e.preventDefault();
		const drawerName = e.target.getAttribute('data-drawer');
		openDrawer(drawerName);
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
	const drawer = DRAWERS[drawerName];

	if (Object.keys(data).length > 0) {
		drawer.setState(data, {
			update: false,
		});
	}

	console.log('drawerName:', drawerName);

	if (drawer) {
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
