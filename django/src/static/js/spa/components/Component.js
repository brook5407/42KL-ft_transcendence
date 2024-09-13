import { ajax, ajaxWithAuth } from '../ajax.js';

export const ROOT_ELEMENT = document.getElementById('root');
export const MODAL_CONTAINER = document.getElementById('modal-container');
export const DRAWER_CONTAINER = document.getElementById('drawer-container');

export class Component {
	constructor({ state = {}, url = '', props = {}, queryParams = {} } = {}) {
		this.element = null;
		this.state = state;
		this.props = props;
		this.className = '';
		this.queryParams = queryParams;
		this.url = url;
		this.scripts = [];
		this.styles = [];

		this.mounted = false;
		this.wrapper = null;
	}

	async fetchHtml(url, queryParams = {}) {
		try {
			// const urlParams = new URLSearchParams(queryParams);
			// const urlWithParams = url + '?' + urlParams.toString();
			const response = await ajaxWithAuth(url, {
				method: 'GET',
				params: queryParams,
			});
			if (response.status === 404) {
				return `
				<div class="not-found">
					<h1>404</h1>
					<p>Page not found</p>
				</div>
				`;
			}
			const html = await response.text();
			return html;
		} catch {
			return null;
		}
	}

	// render the component
	async render() {
		await this.initComponent();

		if (this.wrapper === null) {
			this.wrapper = document.createElement('div');
		}
		this.wrapper.className = this.className;

		if (this.url !== '') {
			const html = await this.fetchHtml(this.url, this.queryParams);
			this.wrapper.innerHTML = html;
		} else {
			this.wrapper.innerHTML = this.template();
		}

		// Find and execute all script tags
		const scripts = this.wrapper.getElementsByTagName('script');
		for (let i = 0; i < scripts.length; i++) {
			console.log('executing script', scripts[i].src || 'custom script');
			const script = document.createElement('script');
			script.type = scripts[i].type || 'text/javascript';
			if (scripts[i].src) {
				script.src = scripts[i].src;
			} else {
				script.text = scripts[i].innerHTML;
			}
			document.body.appendChild(script);
			this.scripts.push(script);
		}

		// append all css into head, to avoid FOUC
		const links = this.wrapper.querySelectorAll('link[rel="stylesheet"]');
		links.forEach((link) => {
			// Check if the link is already in the <head> to avoid duplicates
			if (!document.querySelector(`head link[href="${link.href}"]`)) {
				const linkClone = link.cloneNode(true);
				document.head.appendChild(linkClone);
				this.styles.push(linkClone);
			}
			link.remove();
		});

		// function areStylesLoaded(styles) {
		// 	return Promise.all(
		// 		styles.map((style) => {
		// 			return new Promise((resolve, reject) => {
		// 				style.onload = () => resolve(style);
		// 				style.onerror = () =>
		// 					reject(new Error(`Failed to load stylesheet: ${style.href}`));
		// 			});
		// 		})
		// 	);
		// }

		// await areStylesLoaded(this.styles);

		this.element = this.wrapper;

		this.startComponent();

		if (!this.mounted) {
			this.componentMounted();
		}

		return this.wrapper;
	}

	// Destroy element
	destroy() {
		if (this.element) {
			this.cleanupComponent();
			this.element.remove();
		}
	}

	// Set the state and re-render the component
	setState(newState, options = { update: true }) {
		this.state = { ...this.state, ...newState };
		if (options.update === true) {
			this.update();
		}
	}

	// Update the component
	async update() {
		if (this.element) {
			const newElement = await this.render();
			this.element.replaceWith(newElement);
			this.element = newElement;
		}
	}

	async initComponent() {}

	startComponent() {}

	componentMounted() {
		this.mounted = true;
	}

	cleanupComponent() {
		this.scripts.forEach((script) => {
			console.log('removing script', script.src || 'custom script');
			script.remove();
		});
		this.styles.forEach((link) => {
			console.log('removing link', link.href);
			link.remove();
		});
	}

	// Template method (override this method in subclasses)
	template() {
		return '<div></div>';
	}
}
