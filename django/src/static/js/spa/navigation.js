export const ROUTES = {
	'/': 'home',
	'/login': 'login',
	'/register': 'register',
	'/pong': 'pong',
};

export class Navigation {
	constructor() {
		this.routes = ROUTES;
	}

	getCurrentRoute() {
		return window.location.pathname;
	}

	navigateTo(url) {
		history.pushState(null, null, url);
		navigate();
	}

	async navigate() {
		const currentRoute = getCurrentRoute();
		const route = this.routes[currentRoute];
		// TODO
	}
}
