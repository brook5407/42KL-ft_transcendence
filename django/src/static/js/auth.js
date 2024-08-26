import { showSuccessMessage, showInfoMessage } from './message.js';
import { closeModal } from './spa/modal.js';
import { router } from './spa/navigation.js';
import { ajax, ajax_with_auth } from './spa/ajax.js';
import { closeDrawer } from './spa/drawer.js';

export function signup(data) {
	closeModal();
	showSuccessMessage('Please check your email to verify your account!');
	router();
}

export function signin(data) {
	localStorage.setItem('access_token', data.access);
	localStorage.setItem('refresh_token', data.refresh);
	getCurrentUser();
	showSuccessMessage('You have successfully signed in!');
	closeModal();
	router();
}

export function logout() {
	localStorage.removeItem('access_token');
	localStorage.removeItem('refresh_token');
	clearCurrentUser();
	showInfoMessage('You have successfully logged out!');
	closeDrawer();
	router();
}

export function getCurrentUser() {
	return ajax_with_auth('/current-user', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
		},
	})
		.then((response) => {
			if (response.ok) {
				return response.json();
			}
		})
		.then((data) => {
			window.currentUser = data;
			const event = new CustomEvent('user-ready');
			document.dispatchEvent(event);
			return data;
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

document.addEventListener('DOMContentLoaded', function () {
	document.body.addEventListener('click', function (event) {
		if (event.target.matches('#logout-button')) {
			ajax('/auth/signout', {
				method: 'POST',
			}).then((response) => {
				if (response.ok) {
					logout();
				}
			});
		}
	});
});


