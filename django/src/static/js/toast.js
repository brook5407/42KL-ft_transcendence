const TOAST_CONTAINER = document.getElementById('toast-container');

function showToast(message, title, image = null, type, toOpen = null) {
	const toast = document.createElement('div');
	toast.classList.add('toast-box', type);

	const content = `
		<div class="toast-header">
			${image ? `<img src="${image}" alt="Avatar" class="toast-avatar">` : ''}
            <span>${title}</span>
            <button class="toast-close-button">
				<i class="fa fa-times"></i>
			</button>
        </div>
        <div class="toast-body">
            <span>${message}</span>
			${toOpen ? '<i class="fa fa-link toast-link-icon"></i>' : ''}
        </div>
		<div class="toast-progress-bar"></div>
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

	// Wait for the toast to be added to the DOM and show it
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

	const duration = 5000;
	animateProgressBar(toast, duration);
	setTimeout(closeToast, duration + 100);
}

function animateProgressBar(toast, duration) {
	const progressBar = toast.querySelector('.toast-progress-bar');
	let startTime = null;

	const updateProgressBar = (timestamp) => {
		if (!startTime) startTime = timestamp;
		const elapsed = timestamp - startTime;
		const progress = Math.min((elapsed / duration) * 100, 100);
		progressBar.style.width = `${100 - progress}%`;
		if (elapsed < duration) {
			requestAnimationFrame(updateProgressBar);
		}
	};

	requestAnimationFrame(updateProgressBar);
}

export function showSuccessToast(
	message,
	title = 'Success!',
	image = null,
	toOpen = null
) {
	showToast(message, title, image, 'success', toOpen);
}

export function showErrorToast(
	message,
	title = 'Error!',
	image = null,
	toOpen = null
) {
	showToast(message, title, image, 'error', toOpen);
}

export function showInfoToast(
	message,
	title = 'Notice!',
	image = null,
	toOpen = null
) {
	showToast(message, title, image, 'info', toOpen);
}

window.showSuccessToast = showSuccessToast;
window.showErrorToast = showErrorToast;
window.showInfoToast = showInfoToast;
