import { DRAWER_CONTAINER } from './components/component.js';
import { GenericDrawer } from './components/drawer/generic.js';
import { ChatRoom } from './components/drawer/chat-room.js';
import { ChatList } from './components/drawer/chat-list.js';

class DrawerStack {
	constructor() {
		/**
		 * The stack of drawers.
		 * every element in the stack stores the drawer name and drawer url
		 * @type {Array<{drawerName: string, drawerUrl: string}>}
		 */
		this.stack = [];
	}

	/**
	 * Push a drawer onto the stack.
	 * @param {string} drawerName - The name of the drawer.
	 * @param {string} drawerUrl - The URL of the drawer.
	 */
	push(drawerName, drawerUrl) {
		this.stack.push({
			drawerName,
			drawerUrl,
		});
	}

	/**
	 * Pop a drawer from the stack.
	 * @returns {void}
	 */
	pop() {
		this.stack.pop();
	}

	empty() {
		this.stack = [];
	}

	/**
	 * Get the current drawer from the stack.
	 * @returns {{drawerName: string, drawerUrl: string}|undefined} The current drawer or undefined if the stack is empty.
	 */
	getCurrentDrawer() {
		if (this.stack.length === 0) {
			return undefined;
		}
		return this.stack[this.stack.length - 1];
	}
}

let currentDrawer = null;
const drawerStack = new DrawerStack();

export const DRAWERS = {
	profile: GenericDrawer,
	settings: GenericDrawer,
	'chat-list': ChatList,
	'chat-room': ChatRoom,
	'friend-list': GenericDrawer,
	'friend-requests': GenericDrawer,
	'search-friend': GenericDrawer,
	'friend-profile': GenericDrawer,
	'friend-room': GenericDrawer,
};

// open drawer and back buttons handler
document.body.addEventListener('click', (e) => {
	if (e.target.matches('[data-drawer]')) {
		// open drawer
		e.preventDefault();
		const drawerName = e.target.getAttribute('data-drawer');
		const drawerUrl = e.target.getAttribute('data-drawer-url') || '';
		openDrawer(drawerName, { url: drawerUrl });
	} else if (e.target.matches('.drawer-back-btn')) {
		// open the previous drawer
		e.preventDefault();
		currentDrawer?.destroy();
		drawerStack.pop();
		const drawerToOpen = drawerStack.getCurrentDrawer();
		if (drawerToOpen) {
			openDrawer(
				drawerToOpen.drawerName,
				{ url: drawerToOpen.drawerUrl },
				false
			);
		}
	}
});

function dispatchDrawerOpenedEvent(e = null) {
	document.dispatchEvent(new CustomEvent('drawer-opened', e));
}

export async function openDrawer(drawerName, data = {}, pushStack = true) {
	const drawerClass = DRAWERS[drawerName];
	const drawer = new drawerClass({
		url: data.url,
		state: data.state || {},
	});

	console.log('drawerName:', drawerName);

	if (!drawer) {
		console.error('Drawer not found:', drawerName);
		return;
	}

	currentDrawer = drawer;
	if (pushStack) {
		drawerStack.push(drawerName, data.url);
	}
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
}

export function closeDrawer() {
	const drawerOverlay = document.getElementById('drawerOverlay');
	const drawer = document.getElementById('drawer');
	drawerOverlay?.classList.remove('drawer-active');
	drawer?.classList.remove('drawer-active');
	setTimeout(() => {
		DRAWER_CONTAINER.innerHTML = '';
		currentDrawer?.destroy();
	}, 500);
	drawerStack.empty();
}

function activateDrawer() {
	const drawerOverlay = document.getElementById('drawerOverlay');
	const drawer = document.getElementById('drawer');
	drawerOverlay.classList.add('drawer-active');
	drawer.classList.add('drawer-active');

	document
		.getElementById('drawerOverlay')
		.addEventListener('click', closeDrawer);
}

// Expose the openDrawer and closeDrawer functions to the global scope
window.openDrawer = openDrawer;
window.closeDrawer = closeDrawer;
