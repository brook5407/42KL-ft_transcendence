import { HomePage } from './components/pages/home.js';
import { NotFoundPage } from './components/pages/not_found.js';
import { ROOT_ELEMENT } from './components/component.js';
import { PongPage } from './components/pages/pong.js';


export const ROUTES = {
	'/': {
		component: HomePage,
		data: { url: '/home' }
	},
	'/pong/index': {
		component: PongPage,
		data: { url: '/pong/index/' }
	},
	'/pong/pvp': {
		component: PongPage,
		data: { url: '/pong/pvp/' }
	},
	'/pong/pve': {
		component: PongPage,
		data: { url: '/pong/pve/' }
	},
	'/pong/tournament': {
		component: PongPage,
		data: { url: '/pong/tournament/' }
	},
	'^\/pong\/tournament\/[^\/]+\/?$': {
		component: PongPage,
		dynamic: true,
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

export async function router() {
	// remove trailing slash
	let pathname = window.location.pathname;
	if (pathname.length > 1 && pathname[pathname.length - 1] === '/') {
		pathname = pathname.slice(0, -1);
	}

	let match = ROUTES[pathname];
	if (!match) {
		// try regular expression match
		for (const pattern in ROUTES) {
			if (!ROUTES[pattern].dynamic) {
				continue;
			}
			console.log(pattern)
			console.log(pathname)
			const re = new RegExp(pattern);
			if (re.test(pathname)) {
				match = ROUTES[pattern];
				console.log(match)
				break;
			}
		}
	}

	let component;
	if (!match) {
		component = new NotFoundPage({});
	} else if (match.dynamic) {
		console.log(pathname)
		component = new match.component({ url: pathname });
	} else {
		component = new match.component(match.data);
	}

	window.currentRootComponent?.destroy();
	window.currentRootComponent = component;
	const element = await component.render();
	ROOT_ELEMENT.innerHTML = '';
	ROOT_ELEMENT.appendChild(element);
}

export function navigateTo(url, title = 'AIsPong') {
	history.pushState(null, null, url);
	router();
	document.title = title;
}

window.navigateTo = navigateTo;
