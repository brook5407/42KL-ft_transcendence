import { MODAL_CONTAINER } from './components/Component.js';
import { SignIn } from './components/modals/SignIn.js';
import { SignUp } from './components/modals/SignUp.js';
import { Oauth42 } from './components/modals/Oauth42.js';
import { ForgetPassword } from './components/modals/ForgetPassword.js';
import { ResetPassword } from './components/modals/ResetPassword.js';
import { checkNearestMatch } from './utils.js';

let currentModal = null;

export const MODALS = {
	signin: SignIn,
	signup: SignUp,
	oauth42: Oauth42,
	forgetpassword: ForgetPassword,
	resetpassword: ResetPassword,
};

// open modal buttons handler
document.body.addEventListener('click', (e) => {
	const modalElement = checkNearestMatch(e.target, '[data-modal]', 3);
	if (modalElement) {
		e.preventDefault();
		const modalName = modalElement.getAttribute('data-modal');
		const url = modalElement.getAttribute('data-modal-url') || '';
		const stateStr = modalElement.getAttribute('data-state');
		const state = stateStr ? JSON.parse(stateStr) : {};
		const propsStr = modalElement.getAttribute('data-props');
		const props = propsStr ? JSON.parse(propsStr) : {};
		const queryParamsStr = modalElement.getAttribute('data-query-params');
		const queryParams = queryParamsStr ? JSON.parse(queryParamsStr) : {};
		openModal(modalName, {
			url,
			state,
			props,
			queryParams,
		});
	}
});

export async function openModal(modalName, data = {}) {
	const modalClass = MODALS[modalName];
	data.name = modalName;
	const modal = new modalClass(data);

	console.log('modalName:', modalName);

	if (modal) {
		currentModal = modal;
		const element = await modal.render();
		MODAL_CONTAINER.innerHTML = '';
		MODAL_CONTAINER.appendChild(element);
		setTimeout(() => {
			activateModal();
			dispatchModalOpenedEvent({
				detail: modalName,
			});
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

function dispatchModalOpenedEvent(e = null) {
	document.dispatchEvent(new CustomEvent('modal-opened'), e);
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
