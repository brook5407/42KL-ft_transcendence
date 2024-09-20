import { ajax, ajaxWithAuth } from './ajax.js';
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
			} else if (event.target.matches('#reset-password-form')) {
				submitForm(event.target, method, (data) => {
					window.location.href = '/';
				});
			} else {
				submitForm(event.target, method);
			}
		}
	});
});

function submitForm(form, method = 'POST', callback) {
	const formData = new FormData(form); // Collect form data
	const actionUrl = form.getAttribute('action') || form.dataset.route; // Determine the submission URL

	const closeLoadingEffect = showLoadingEffect(); // Show the loading effect

	// Send the form data using Fetch API
	ajaxWithAuth(actionUrl, {
		method: method,
		body: formData,
		headers: {
			Accept: 'application/json',
			// Additional headers can be added here
		},
	})
		.then((response) => {
			if (!response.ok && response.status != 204) {
				// Handle non-200 responses
				return response.json().then((errorData) => {
					// Extract error message(s)
					let errorMessage = 'An error occurred';
					if (errorData.non_field_errors) {
						errorMessage = errorData.non_field_errors.join(' ');
					}else if (errorData.detail) {
						errorMessage = errorData.detail;
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
			closeLoadingEffect(); // Remove the loading effect
			if (callback) {
				callback(data);
			} else {
				showSuccessMessage('Operation successful');
			}
		})
		.catch((error) => {
			closeLoadingEffect(); // Remove the loading effect
			console.error('Error:', error);
			showErrorMessage(error.message);
		});
}
