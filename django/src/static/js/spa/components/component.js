const ROOT_ELEMENT = document.getElementById('root');

class Component {
	constructor({ props = {}, children = [], className = '', state = {} }) {
		this.element = null;
		this.props = props;
		this.className = className;
		this.state = state;
		this.children = children;
	}

	async fetchHtml(url, options) {
		try {
			const response = await fetch(url, options);
			const html = await response.text();
			return html;
		} catch {
			return null;
		}
	}

	// render the component
	async render(url = '') {
		const wrapper = document.createElement('div');
		wrapper.className = this.className;

		if (url) {
			const html = await this.fetchHtml(url);
			wrapper.innerHTML = html;
		} else {
			wrapper.innerHTML = this.template();
		}

		this.element = wrapper;
		this.children.forEach((child) => {
			const childElement = child.render();
			wrapper.appendChild(childElement);
		});

		this.addEventListeners();
		return wrapper;
	}

	// Destroy element
	destroy() {
		if (this.element) {
			this.element.destroyEventListeners();
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

	addEventListeners() {
		// To be implemented by subclasses
	}

	destroyEventListeners() {
		// To be implemented by subclasses
	}

	// Template method (override this method in subclasses)
	template() {
		return '<div></div>';
	}
}
