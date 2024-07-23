const MESSAGE_CONTAINER = document.getElementById('message-container');

function showMessage(message, type) {
	MESSAGE_CONTAINER.innerHTML = ''; // Clear any existing messages
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
		setTimeout(() => MESSAGE_CONTAINER.removeChild(messageBox), 500); // Wait for fade out to finish
	}, 3000);
}

export function showSuccessMessage(message) {
	showMessage(message, 'success');
}

export function showErrorMessage(message) {
	showMessage(message, 'error');
}
