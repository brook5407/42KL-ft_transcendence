const TOAST_CONTAINER = document.getElementById('toast-container');

function showToast(message, title, type, toOpen = null) {
	const toast = document.createElement('div');
	toast.classList.add('toast-box', type);

	const content = `
		<div class="toast-header">
            <span>${title}</span>
            <button class="toast-close-button">
				<i class="fa fa-times"></i>
			</button>
        </div>
        <div class="toast-body">
            <span>${message}</span>
			${toOpen ? '<i class="fa fa-link toast-link-icon"></i>' : ''}
        </div>
	`;
	toast.innerHTML = content;

	const closeToast = () => {
		toast.classList.remove('show');
		setTimeout(() => {
			TOAST_CONTAINER.contains(toast) && TOAST_CONTAINER.removeChild(toast);
		}, 500); // Wait for fade out to finish
	};

	const closeButton = toast.querySelector('button.toast-close-button');
	closeButton.addEventListener('click', closeToast);

	TOAST_CONTAINER.innerHTML = '';
	TOAST_CONTAINER.appendChild(toast);

	setTimeout(() => {
		toast.classList.add('show');
	}, 100);

	if (toOpen) {
		const jumpIcon = toast.querySelector('.toast-link-icon');
		jumpIcon.classList.add('clickable');
		jumpIcon.addEventListener('click', () => {
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

export function showSuccessToast(message, title = 'Notice!', toOpen = null) {
	showToast(message, title, 'success', toOpen);
}

export function showErrorToast(message, title = 'Notice!', toOpen = null) {
	showToast(message, title, 'error', toOpen);
}

export function showInfoToast(message, title = 'Notice!', toOpen = null) {
	showToast(message, title, 'info', toOpen);
}

window.showSuccessToast = showSuccessToast;
window.showErrorToast = showErrorToast;
window.showInfoToast = showInfoToast;
