import { MODAL_CONTAINER } from './components/component.js';
import { SignIn } from './components/modals/signin.js';
import { SignUp } from './components/modals/signup.js';
import { Oauth42 } from './components/modals/42oauth.js';

let currentModal = null;

export const MODALS = {
	signin: SignIn,
	signup: SignUp,
	oauth42: Oauth42,
};

// open modal buttons handler
document.body.addEventListener('click', (e) => {
	if (e.target.matches('[data-modal]')) {
		e.preventDefault();
		const modalName = e.target.getAttribute('data-modal');
		const modalUrl = e.target.getAttribute('data-modal-url') || '';
		openModal(modalName, { url: modalUrl });
	}
});

export async function openModal(modalName, data = {}) {
	const modalClass = MODALS[modalName];
	const modal = new modalClass({
		url: data.url,
		state: data.state,
	});

	console.log('modalName:', modalName);

	if (modal) {
		currentModal = modal;
		const element = await modal.render();
		MODAL_CONTAINER.innerHTML = '';
		MODAL_CONTAINER.appendChild(element);
		setTimeout(() => {
			activateModal();
		}, 100);
	} else {
		console.error('Modal not found:', modalName);
	}
}

export function closeModal() {
	const modalOverlay = document.getElementById('modalOverlay');
	const modal = document.getElementById('modal');
	modalOverlay?.classList.remove('modal-active');
	modal?.classList.remove('modal-active');
	setTimeout(() => {
		MODAL_CONTAINER.innerHTML = '';
		currentModal?.destroy();
	}, 500);
}

function activateModal() {
	const modalOverlay = document.getElementById('modalOverlay');
	const modal = document.getElementById('modal');
	modalOverlay?.classList.add('modal-active');
	modal?.classList.add('modal-active');

	document
		.getElementById('closeModalBtn')
		.addEventListener('click', closeModal);

	document.getElementById('modalOverlay').addEventListener('click', closeModal);
}
