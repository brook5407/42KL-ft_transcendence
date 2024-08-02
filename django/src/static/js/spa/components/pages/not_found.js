import { Component } from '../component.js';

export class NotFoundPage extends Component {
	constructor(params) {
		super(params);
		if (this.url === '') {
			this.url = '/not-found';
		}
	}

	template() {
		return `
	  <div class="not-found">
		<h1>404</h1>
		<p>Page not found</p>
	  </div>
	`;
	}
}
