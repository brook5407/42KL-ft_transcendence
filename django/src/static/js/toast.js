const TOAST_CONTAINER = document.getElementById('toast-container');

function showToast(message, type, toOpen = null) {
	const toast = document.createElement('div');
	toast.classList.add('toast', type);
	const textBox = document.createElement('span');
	textBox.textContent = message;

	// if the toast can be clicked to open a drawer or modal, add underline to the text
	if (toOpen) {
		textBox.classList.add('underline-text');
	}

	const closeToast = () => {
		toast.classList.remove('fade-in');
		setTimeout(() => {
			TOAST_CONTAINER.contains(toast) && TOAST_CONTAINER.removeChild(toast);
		}, 500); // Wait for fade out to finish
	};

	// add a close button
	const closeButton = document.createElement('span');
	closeButton.classList.add('toast-close-button');
	closeButton.innerHTML = '&times;';
	closeButton.addEventListener('click', closeToast);

	toast.appendChild(textBox);
	toast.appendChild(closeButton);
	TOAST_CONTAINER.appendChild(toast);

	setTimeout(() => {
		toast.classList.add('fade-in');
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
			closeToast();
		});
	}

	// Remove the toast after 5 seconds
	setTimeout(closeToast, 5000);
}

export function showSuccessToast(message, toOpen = null) {
	showToast(message, 'success', toOpen);
}

export function showErrorToast(message, toOpen = null) {
	showToast(message, 'error', toOpen);
}

export function showInfoToast(message, toOpen = null) {
	showToast(message, 'info', toOpen);
}

window.showSuccessToast = showSuccessToast;
window.showErrorToast = showErrorToast;
window.showInfoToast = showInfoToast;
