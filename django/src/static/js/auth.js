import { showSuccessMessage, showInfoMessage } from './message.js';
import { closeModal } from './spa/modal.js';
import { router } from './spa/navigation.js';
import { ajax } from './spa/ajax.js';
import { closeDrawer } from './spa/drawer.js';

export function signup(data) {
	closeModal();
	showSuccessMessage('You have successfully signed up!');
	router();
}

export function signin(data) {
	localStorage.setItem('access_token', data.access);
	localStorage.setItem('refresh_token', data.refresh);

	closeModal();
	showSuccessMessage('You have successfully signed in!');
	router();
}

export function logout() {
	localStorage.removeItem('access_token');
	localStorage.removeItem('refresh_token');
	showInfoMessage('You have successfully logged out!');
	closeDrawer();
	router();
}

document.addEventListener('DOMContentLoaded', function () {
	document.body.addEventListener('click', function (event) {
		if (event.target.matches('#logout-button')) {
			ajax('/auth/signout', {
				method: 'POST',
			})
			.then((response) => {
				if (response.ok) {
					logout();
				}
			});
		}
	});
});
