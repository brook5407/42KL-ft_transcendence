import { HomePage } from './components/pages/HomePage.js';
import { NotFoundPage } from './components/pages/NotFoundPage.js';
import { ROOT_ELEMENT } from './components/Component.js';
import { PongPage } from './components/pages/PongPage.js';

export const ROUTES = {
	'/': {
		component: HomePage,
		data: { url: '/home' },
	},
	'/pong/index': {
		component: PongPage,
		data: { url: '/pong/index/' },
	},
	'/pong/pvp': {
		component: PongPage,
		data: { url: '/pong/pvp/' },
	},
	'/pong/pve': {
		component: PongPage,
		data: { url: '/pong/pve/' },
	},
	'/pong/tournament': {
		component: PongPage,
		data: { url: '/pong/tournament/' },
	},
};

// global variable to keep track of the current root component
window.currentRootComponent = null;

// listen to the back button
window.addEventListener('popstate', router);

// SPA link handler
document.body.addEventListener('click', (e) => {
	if (e.target.matches('[data-link]')) {
		e.preventDefault();
		navigateTo(e.target.href);
	}
});

export async function router(data) {
	// remove trailing slash
	let pathname = data?.url || window.location.pathname;
	if (pathname.length > 1 && pathname[pathname.length - 1] === '/') {
		pathname = pathname.slice(0, -1);
	}

	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const queryParams = {};
	urlParams.forEach((value, key) => {
		queryParams[key] = value;
	});

	let match = ROUTES[pathname];
	if (!match) {
		// try regular expression match
		for (const pattern in ROUTES) {
			if (!ROUTES[pattern].dynamic) {
				continue;
			}
			const re = new RegExp(pattern);
			if (re.test(pathname)) {
				match = ROUTES[pattern];
				break;
			}
		}
	}

	let component;
	if (!match) {
		component = new NotFoundPage({});
	} else if (match.dynamic) {
		component = new match.component({ url: pathname, queryParams });
	} else {
		component = new match.component({ ...match.data, queryParams });
	}

	window.currentRootComponent?.destroy();
	window.currentRootComponent = component;
	const element = await component.render();
	ROOT_ELEMENT.innerHTML = '';
	ROOT_ELEMENT.appendChild(element);
	document.dispatchEvent(new Event('page-loaded'));
}

export function navigateTo(url, title = 'AIsPong') {
	if (typeof window.closeDrawer === 'function') {
		window.closeDrawer();
	}

	if (typeof window.closeModal === 'function') {
		window.closeModal();
	}
	history.pushState(null, null, url);
	router();
	document.title = title;
}

window.navigateTo = navigateTo;
