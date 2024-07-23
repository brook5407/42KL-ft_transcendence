import { ajax } from './ajax.js';
import { showSuccessMessage, showErrorMessage } from '../message.js';

document.addEventListener('DOMContentLoaded', function () {
	// Attach the event listener to the document or a parent element that exists at page load
	document.body.addEventListener('submit', function (event) {
		// Check if the target of the submit event matches .spa-form
		if (event.target.matches('.spa-form')) {
			event.preventDefault(); // Prevent the default form submission

			const form = event.target;
			const formData = new FormData(form); // Collect form data
			const actionUrl = form.getAttribute('action') || form.dataset.route; // Determine the submission URL

			// Send the form data using Fetch API
			ajax(actionUrl, {
				method: 'POST',
				body: formData,
				headers: {
					Accept: 'application/json',
					// Additional headers can be added here
				},
			})
				.then((response) => response.json())
				.then((data) => {
					if (data.status === 'error') {
						showErrorMessage(data.message);
					} else {
						showSuccessMessage(data.message);
					}
				})
				.catch((error) => {
					console.error('Error:', error);
					showErrorMessage(error.message);
				});
		}
	});
});
