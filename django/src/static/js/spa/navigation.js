import { HomePage } from './components/home.js';
import { NotFoundPage } from './components/not_found.js';
import { ROOT_ELEMENT } from './components/component.js';

export const ROUTES = {
	'/': new HomePage({ url: 'home' }),
	'/login': 'login',
	'/register': 'register',
	'/pong': 'pong',
	'/404': new NotFoundPage({}),
};

export class Navigation {
	constructor() {
		this.routes = ROUTES;
		this.currentRouteComponent = this.getCurrentRoute();
	}

	getCurrentRoute() {
		const routeString = window.location.pathname;
		const currentRouteComponent = this.routes[routeString];
		if (!currentRouteComponent) {
			return null;
		}
		return currentRouteComponent;
	}

	async navigateTo(url, title) {
		if (this.currentRouteComponent) {
			this.currentRouteComponent.destroy();
		}
		if (await this.navigate()) {
			history.pushState(null, null, url);
			this.changeTitle(title);
			return;
		}
		this.currentRouteComponent = this.routes['/404'];
		history.pushState(null, null, '/404');
		this.changeTitle('404');
		this.swapRootComponent(await this.currentRouteComponent.render());
	}

	async navigate() {
		const currentRouteComponent = this.getCurrentRoute();
		if (!currentRouteComponent) {
			return false;
		}
		this.currentRouteComponent = currentRouteComponent;
		const element = await this.currentRouteComponent.render();
		this.swapRootComponent(element);
		return true;
	}

	swapRootComponent(component) {
		ROOT_ELEMENT.innerHTML = '';
		ROOT_ELEMENT.appendChild(component);
	}

	changeTitle(title) {
		document.title = title;
	}
}
