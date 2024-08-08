import { Component } from '../component.js';

export class NotFoundPage extends Component {
	constructor(params) {
		super(params);
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
