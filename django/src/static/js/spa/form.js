import { ajax, ajax_with_auth } from './ajax.js';
import { showSuccessMessage, showErrorMessage } from '../message.js';
import { signin, signup } from '../auth.js';

document.addEventListener('DOMContentLoaded', function () {
	// Attach the event listener to the document or a parent element that exists at page load
	document.body.addEventListener('submit', function (event) {
		// Check if the target of the submit event matches .spa-form
		if (event.target.matches('.spa-form')) {
			event.preventDefault(); // Prevent the default form submission
			const method = event.target.getAttribute('method') || 'POST'; // Determine the form submission method

			if (event.target.matches('#signin-form')) {
				submitForm(event.target, method, signin);
			} else if (event.target.matches('#signup-form')) {
				submitForm(event.target, method, signup);
			} else {
				submitForm(event.target, method);
			}
		}
	});
});

function submitForm(form, method = "POST", callback) {
	const formData = new FormData(form); // Collect form data
	const actionUrl = form.getAttribute('action') || form.dataset.route; // Determine the submission URL

	// Send the form data using Fetch API
	ajax_with_auth(actionUrl, {
		method: method,
		body: formData,
		headers: {
			Accept: 'application/json',
			// Additional headers can be added here
		},
	})
		.then((response) => {
			console.log(response);
			if (!response.ok && response.status != 204) {
				// Handle non-200 responses
				return response.json().then((errorData) => {
					// Extract error message(s)
					let errorMessage = 'An error occurred';
					if (errorData.non_field_errors) {
						errorMessage = errorData.non_field_errors.join(' ');
					} else {
						// Handle field-specific errors
						const fieldErrors = [];
						for (const [field, messages] of Object.entries(errorData)) {
							fieldErrors.push(`${messages.join('')}`);
						}
						errorMessage = fieldErrors.join('\n');
					}
					throw new Error(errorMessage);
				});
			}
			return response.json();
		})
		.then((data) => {
			if (callback) {
				callback(data);
			} else {
				showSuccessMessage('Operation successful');
			}
		})
		.catch((error) => {
			console.error('Error:', error);
			showErrorMessage(error.message);
		});
}
