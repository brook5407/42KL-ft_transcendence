import { showSuccessMessage, showInfoMessage } from './message.js';
import { closeModal } from './spa/modal.js';
import { router } from './spa/navigation.js';
import { ajax, ajaxWithAuth } from './spa/ajax.js';
import { closeDrawer } from './spa/drawer.js';

export function signup(data) {
	closeModal();
	showSuccessMessage('Please check your email to verify your account!');
	router();
}

export function signin(data) {
	getCurrentUser();
	showSuccessMessage('You have successfully signed in!');
	closeModal();
	router();
}

export function logout() {
	clearCurrentUser();
	showInfoMessage('You have successfully logged out!');
	closeDrawer();
	router();
}

export function getCurrentUser() {
	return ajaxWithAuth('/current-user', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
		},
	})
		.then((response) => {
			if (response.ok) {
				return response.json();
			} else {
				throw 'User not logged in';
			}
		})
		.then(
			/** @param {CurrentUser} data */
			(data) => {
				window.currentUser = data;
				const event = new CustomEvent('user-ready');
				document.dispatchEvent(event);
				return data;
			}
		)
		.catch((error) => {
			console.log(error);
		});
}

export function clearCurrentUser() {
	window.currentUser = null;
	// dispatch user-cleared event
	const event = new CustomEvent('user-cleared');
	document.dispatchEvent(event);
}

export function checkAuth() {
	return window.currentUser;
}

window.getCurrentUser = getCurrentUser;
window.clearCurrentUser = clearCurrentUser;
window.checkAuth = checkAuth;

document.addEventListener('DOMContentLoaded', function () {
	document.body.addEventListener('click', function (event) {
		if (event.target.matches('#logout-button')) {
			const isOauth = getCookie('is_oauth');
			ajax('/auth/signout', {
				method: 'POST',
			}).then((response) => {
				if (response.ok) {
					logout();
					if (isOauth) {
						deleteCookie('is_oauth');
						// deleteCookie('access_token');
						// deleteCookie('refresh_token');
					}
				}
			});
		}
	});
});
