import { DRAWER_CONTAINER } from './components/component.js';
import { Profile } from './components/drawer/profile.js';

export const DRAWERS = {
	profile: new Profile({ url: '/drawer/profile' }),
};

// open drawer buttons handler
document.body.addEventListener('click', (e) => {
	if (e.target.matches('[data-drawer]')) {
		e.preventDefault();
		const drawerName = e.target.getAttribute('data-drawer');
		console.log('drawerName:', drawerName);
		openDrawer(drawerName);
	}
});

export async function openDrawer(drawerName) {
	const drawer = DRAWERS[drawerName];
	if (drawer) {
		const element = await drawer.render();
		DRAWER_CONTAINER.innerHTML = '';
		DRAWER_CONTAINER.appendChild(element);
		setTimeout(() => {
			activateDrawer();
		}, 100);
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

	document.getElementById('drawerOverlay').addEventListener('click', closeDrawer);
}
