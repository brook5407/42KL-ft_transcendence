const MESSAGE_CONTAINER = document.getElementById('message-container');

function showMessage(message, type, toOpen = null) {
	const messageBox = document.createElement('div');
	messageBox.classList.add('toast-box', type);
	const textBox = document.createElement('span');
	textBox.textContent = message;

	// if the message box can be clicked to open a drawer or modal, add underline to the text
	if (toOpen) {
		textBox.classList.add('underline-text');
	}

	const closeMessageBox = () => {
		messageBox.classList.remove('fade-in');
		setTimeout(() => {
			MESSAGE_CONTAINER.contains(messageBox) &&
				MESSAGE_CONTAINER.removeChild(messageBox);
		}, 500); // Wait for fade out to finish
	};

	// add a close button
	const closeButton = document.createElement('span');
	closeButton.classList.add('message-close-button');
	closeButton.innerHTML = '&times;';
	closeButton.addEventListener('click', closeMessageBox);

	messageBox.appendChild(textBox);
	messageBox.appendChild(closeButton);
	MESSAGE_CONTAINER.appendChild(messageBox);

	setTimeout(() => {
		messageBox.classList.add('fade-in');
	}, 100);

	if (toOpen) {
		textBox.classList.add('clickable');
		textBox.addEventListener('click', () => {
			const toOpenType = toOpen?.type;
			if (toOpenType === 'page') {
				window.location.href = toOpen?.url;
			} else if (toOpenType === 'drawer') {
				openDrawer(toOpen?.name, toOpen?.data);
			} else if (toOpenType === 'modal') {
				openModal(toOpen?.name, toOpen?.data);
			}
			closeMessageBox();
		});
	}

	// Remove the message after 5 seconds
	setTimeout(closeMessageBox, 5000);
}

export function showSuccessMessage(message, toOpen = null) {
	showMessage(message, 'success', toOpen);
}

export function showErrorMessage(message, toOpen = null) {
	showMessage(message, 'error', toOpen);
}

export function showInfoMessage(message, toOpen = null) {
	showMessage(message, 'info', toOpen);
}

document.addEventListener('DOMContentLoaded', () => {
	// Retrieve the JSON data from the script tag
	const flashMessagesElement = document.getElementById('flash-messages');
	if (!flashMessagesElement) {
		return;
	}

	const flashMessages = JSON.parse(flashMessagesElement.textContent);
	if (!flashMessages || flashMessages.length === 0) {
		return;
	}

	// Display all flash messages
	flashMessages.forEach((message) => {
		const messageText = message.message;
		const messageType = message.tags;
		showMessage(messageText, messageType);
	});
});

window.showSuccessMessage = showSuccessMessage;
window.showErrorMessage = showErrorMessage;
window.showInfoMessage = showInfoMessage;
