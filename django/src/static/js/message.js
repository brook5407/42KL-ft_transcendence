const MESSAGE_CONTAINER = document.getElementById('message-container');

function showMessage(message, type) {
	// WXR TODO: add options for go to a specific page, drawer, or modal etc.
	// MESSAGE_CONTAINER.innerHTML = ''; // Clear any existing messages
	const messageBox = document.createElement('div');
	messageBox.classList.add('message-box', type);
	messageBox.textContent = message;

	MESSAGE_CONTAINER.appendChild(messageBox);

	setTimeout(() => {
		messageBox.classList.add('fade-in');
	}, 100);

	// Remove the message after 5 seconds
	setTimeout(() => {
		messageBox.classList.remove('fade-in');
		setTimeout(() => {
			MESSAGE_CONTAINER.contains(messageBox) &&
				MESSAGE_CONTAINER.removeChild(messageBox);
		}, 500); // Wait for fade out to finish
	}, 5000);
}

export function showSuccessMessage(message) {
	showMessage(message, 'success');
}

export function showErrorMessage(message) {
	showMessage(message, 'error');
}

export function showInfoMessage(message) {
	showMessage(message, 'info');
}

document.addEventListener('DOMContentLoaded', () => {
	// display all django flash messages and delete the input fields
	const flashMessages = document.querySelectorAll('.dj-flash-message');
	flashMessages.forEach((message) => {
		const messageText = message.value;
		const messageType = message.getAttribute('data-message-type');
		showMessage(messageText, messageType);
		message.remove();
	});
});

window.showSuccessMessage = showSuccessMessage;
window.showErrorMessage = showErrorMessage;
window.showInfoMessage = showInfoMessage;
