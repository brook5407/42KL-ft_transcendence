import { ajax, ajax_with_auth } from '../ajax.js';

export const ROOT_ELEMENT = document.getElementById('root');
export const MODAL_CONTAINER = document.getElementById('modal-container');
export const DRAWER_CONTAINER = document.getElementById('drawer-container');

export class Component {
	constructor({ state = {}, url = '' }) {
		this.element = null;
		this.state = state;
		this.queryParams = {};
		this.url = url;
	}

	async fetchHtml(url, queryParams = {}) {
		try {
			const urlParams = new URLSearchParams(queryParams);
			const urlWithParams = url + '?' + urlParams.toString();
			const response = await ajax_with_auth(urlWithParams, {
				method: 'GET',
			});
			const html = await response.text();
			return html;
		} catch {
			return null;
		}
	}

	// render the component
	async render() {
		const wrapper = document.createElement('div');
		wrapper.className = this.className;

		if (this.url !== '') {
			const html = await this.fetchHtml(this.url, this.queryParams);
			wrapper.innerHTML = html;
		} else {
			wrapper.innerHTML = this.template();
		}

		// Find and execute all script tags
		const scripts = wrapper.getElementsByTagName('script');
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
		}

		this.element = wrapper;

		this.initComponent();
		return wrapper;
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

	initComponent() {
		// To be implemented by subclasses
	}

	cleanupComponent() {
		// To be implemented by subclasses
	}

	// Template method (override this method in subclasses)
	template() {
		return '<div></div>';
	}
}
