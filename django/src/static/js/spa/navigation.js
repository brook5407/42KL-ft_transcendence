import { HomePage } from './components/pages/home.js';
import { NotFoundPage } from './components/pages/not_found.js';
import { ROOT_ELEMENT } from './components/component.js';
import { PongPage } from './components/pages/pong.js';

export const ROUTES = {
	'/': new HomePage({ url: '/home' }),
	'/pong/index': new PongPage({ url: '/pong/index/' }),
	'/404': new NotFoundPage({}),
};

// global variable to keep track of the current root component
window.currentRootComponent = ROUTES[window.location.pathname];

// listen to the back button
window.addEventListener('popstate', router);

// SPA link handler
document.body.addEventListener('click', (e) => {
	if (e.target.matches('[data-link]')) {
		e.preventDefault();
		navigateTo(e.target.href);
	}
});

export async function router() {
	// remove trailing slash
	let pathname = window.location.pathname;
	if (pathname.length > 1 && pathname[pathname.length - 1] === '/') {
		pathname = pathname.slice(0, -1);
	}

	let match = ROUTES[pathname];
	if (!match) {
		match = ROUTES['/404'];
	}

	window.currentRootComponent?.destroy();
	window.currentRootComponent = match;
	const element = await match.render();
	ROOT_ELEMENT.innerHTML = '';
	ROOT_ELEMENT.appendChild(element);
}

export function navigateTo(url, title = 'AIsPong') {
	history.pushState(null, null, url);
	router();
	document.title = title;
}
