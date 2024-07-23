import { HomePage } from './components/pages/home.js';
import { NotFoundPage } from './components/pages/not_found.js';
import { ROOT_ELEMENT } from './components/component.js';
import { PongPage } from './components/pages/pong.js';

export const ROUTES = {
	'/': new HomePage({ url: 'home' }),
	'/login': 'login',
	'/register': 'register',
	'/pong': new PongPage({ url: 'pong' }),
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
		console.log('click');
		navigateTo(e.target.href);
	}
});

export async function router() {
	let match = ROUTES[window.location.pathname];
	if (!match) {
		match = ROUTES['/404'];
	}

	window.currentRootComponent = match;
	const element = await match.render();
	ROOT_ELEMENT.innerHTML = '';
	ROOT_ELEMENT.appendChild(element);
}

export function navigateTo(url, title = 'IcePong') {
	window.currentRootComponent?.destroy();
	history.pushState(null, null, url);
	router();
	document.title = title;
}
