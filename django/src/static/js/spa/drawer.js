import { DRAWER_CONTAINER } from './components/Component.js';
import { GenericDrawer } from './components/drawer/GenericDrawer.js';
import { ChatRoomDrawer } from './components/drawer/ChatRoomDrawer.js';
import { ChatListDrawer } from './components/drawer/ChatListDrawer.js';
import { FriendListDrawer } from './components/drawer/FriendListDrawer.js';
import { FriendRequestsDrawer } from './components/drawer/FriendRequestsDrawer.js';
import { checkNearestMatch } from './utils.js';
import { TournamentListDrawer } from './components/drawer/TournamentListDrawer.js';
import { ProfileDrawer } from "./components/drawer/ProfileDrawer.js";
import { FriendProfileDrawer } from "./components/drawer/FriendProfileDrawer.js";

export const DRAWERS = {
	profile: ProfileDrawer,
	settings: GenericDrawer,
	'chat-list': ChatListDrawer,
	'chat-room': ChatRoomDrawer,
	'friend-list': FriendListDrawer,
	'friend-requests': FriendRequestsDrawer,
	'search-friend': GenericDrawer,
	'friend-profile': FriendProfileDrawer,
	'profile-edit': GenericDrawer,
	'match-history': GenericDrawer,
	'tournament-list': TournamentListDrawer,
	'tournament-create': GenericDrawer,
	'tournament-room': GenericDrawer,
};

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
	 * @param {object} drawerData - The data of the drawer.
	 */
	push(drawerName, drawerData) {
		this.stack.push({
			drawerName,
			drawerData,
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

window.currentDrawer = null;
window.drawerStack = new DrawerStack();

// open drawer and back buttons handler
document.body.addEventListener('click', (e) => {
	const drawerElement = checkNearestMatch(e.target, '[data-drawer]', 4);
	if (drawerElement) {
		// open drawer
		e.preventDefault();
		const drawerName = drawerElement.getAttribute('data-drawer');
		const url = drawerElement.getAttribute('data-drawer-url') || '';
		const stateStr = drawerElement.getAttribute('data-state');
		const state = stateStr ? JSON.parse(stateStr) : {};
		const propsStr = drawerElement.getAttribute('data-props');
		const props = propsStr ? JSON.parse(propsStr) : {};
		const queryParamsStr = drawerElement.getAttribute('data-query-params');
		const queryParams = queryParamsStr ? JSON.parse(queryParamsStr) : {};
		openDrawer(drawerName, {
			url,
			state,
			props,
			queryParams,
		});
	} else if (e.target.matches('.drawer-back-btn')) {
		e.preventDefault();
		openPreviousDrawer();
	}
});

function openPreviousDrawer() {
	drawerStack.pop();
	// open the previous drawer
	const drawerToOpen = drawerStack.getCurrentDrawer();
	if (drawerToOpen) {
		openDrawer(drawerToOpen.drawerName, drawerToOpen.drawerData, false);
	} else {
		closeDrawer();
	}
}

function dispatchDrawerOpenedEvent(e = null) {
	document.dispatchEvent(new CustomEvent('drawer-opened', e));
}

export async function openDrawer(drawerName, data = {}, pushStack = true) {
	// close previous drawer only
	closeDrawer(false, false);
	const drawerClass = DRAWERS[drawerName];
	if (!drawerClass) {
		console.error('Drawer not found:', drawerName);
		return;
	}
	data.name = drawerName;
	const drawer = new drawerClass(data);

	// console.log('drawerName:', drawerName);

	if (!drawer) {
		console.error('Drawer not found:', drawerName);
		return;
	}

	currentDrawer = drawer;
	if (pushStack) {
		drawerStack.push(drawerName, data);
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

export function closeDrawer(delay = true, emptyStack = true) {
	const drawerOverlay = document.getElementById('drawerOverlay');
	const drawer = document.getElementById('drawer');
	drawerOverlay?.classList.remove('drawer-active');
	drawer?.classList.remove('drawer-active');

	if (emptyStack) {
		drawerStack.empty();
	}

	if (!delay) {
		// Dispatch the drawer-closed event
		document.dispatchEvent(new CustomEvent('drawer-closed'));
		currentDrawer?.destroy();
		DRAWER_CONTAINER.innerHTML = '';
		currentDrawer = null;
		return;
	}

	setTimeout(() => {
		// Dispatch the drawer-closed event
		document.dispatchEvent(new CustomEvent('drawer-closed'));
		currentDrawer?.destroy();
		DRAWER_CONTAINER.innerHTML = '';
		currentDrawer = null;
	}, 500);
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
window.openPreviousDrawer = openPreviousDrawer;
