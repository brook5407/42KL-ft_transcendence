import { ajax, ajax_with_auth } from '../ajax.js';

export const ROOT_ELEMENT = document.getElementById('root');
export const MODAL_CONTAINER = document.getElementById('modal-container');

export class Component {
	constructor({
		props = {},
		children = [],
		className = '',
		state = {},
		url = '',
	}) {
		this.element = null;
		this.props = props;
		this.className = className;
		this.state = state;
		this.children = children;
		this.url = url;
	}

	async fetchHtml(url) {
		try {
			const response = await ajax_with_auth(url, {
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
			const html = await this.fetchHtml(this.url);
			wrapper.innerHTML = html;
		} else {
			wrapper.innerHTML = this.template();
		}

		this.element = wrapper;
		this.children.forEach((child) => {
			const childElement = child.render();
			wrapper.appendChild(childElement);
		});

		this.initComponent();
		return wrapper;
	}

	// Destroy element
	destroy() {
		if (this.element) {
			this.cleanupComponent();
			this.element.remove();
		}
		this.children.forEach((child) => child.destroy());
	}

	// Set the state and re-render the component
	setState(newState) {
		this.state = { ...this.state, ...newState };
		this.update();
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
