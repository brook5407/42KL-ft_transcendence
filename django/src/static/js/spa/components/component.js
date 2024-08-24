import { ajax, ajax_with_auth } from '../ajax.js';

export const ROOT_ELEMENT = document.getElementById('root');
export const MODAL_CONTAINER = document.getElementById('modal-container');
export const DRAWER_CONTAINER = document.getElementById('drawer-container');

export class Component {
	constructor({ state = {}, url = '', props = {} }) {
		this.element = null;
		this.state = state;
		this.props = props;
		this.className = '';
		this.queryParams = {};
		this.url = url;
		this.scripts = [];

		this.mounted = false;
		this.wrapper = null;
	}

	async fetchHtml(url, queryParams = {}) {
		try {
			// const urlParams = new URLSearchParams(queryParams);
			// const urlWithParams = url + '?' + urlParams.toString();
			const response = await ajax_with_auth(url, {
				method: 'GET',
				params: queryParams,
			});
			const html = await response.text();
			return html;
		} catch {
			return null;
		}
	}

	// render the component
	async render() {
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
	}

	// Template method (override this method in subclasses)
	template() {
		return '<div></div>';
	}
}
