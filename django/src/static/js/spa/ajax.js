import { navigateTo, router } from './navigation.js';

export function ajax(url, options) {
	options.headers = constructRequestHeader(options.headers);

	const fetchOptions = Object.assign(
		{
			method: 'POST',
			credentials: 'same-origin',
		},
		options
	);

	if (
		options.method === 'GET' &&
		options.params &&
		Object.keys(options.params).length > 0
	) {
		const urlParams = new URLSearchParams(options.params);
		url += '?' + urlParams.toString();
	}

	return fetch(url, fetchOptions);
}

export async function ajaxWithAuth(url, options, retries = 0) {
	options.headers = constructRequestHeader(options.headers);

	const accessToken = localStorage.getItem('access_token');
	if (accessToken) {
		options.headers['Authorization'] = `Bearer ${accessToken}`;
	}

	const fetchOptions = Object.assign(
		{
			method: 'POST',
			credentials: 'same-origin',
		},
		options
	);

	if (
		(fetchOptions.method === 'GET' || fetchOptions.method === 'DELETE') &&
		fetchOptions.params &&
		Object.keys(fetchOptions.params).length > 0
	) {
		const urlParams = new URLSearchParams(options.params);
		url += '?' + urlParams.toString();
	}

	const response = await fetch(url, fetchOptions);
	if (response.status === 401) {
		if (retries >= 2) {
			// Redirect to login page
			localStorage.removeItem('access_token');
			localStorage.removeItem('refresh_token');
			deleteCookie('access_token');
			deleteCookie('refresh_token');
			navigateTo('/');
			return response;
		}
		const status = await refreshJWT();
		if (!status) return response;
		// Retry the original request with new access token
		const retryResponse = await ajaxWithAuth(url, options, retries + 1);
		return retryResponse;
	}

	return response;
}

function constructRequestHeader(headers) {
	const csrftoken = document.cookie
		.split('; ')
		?.find((row) => row.startsWith('csrftoken='))
		?.split('=')[1];

	return {
		'X-Requested-With': 'XMLHttpRequest',
		'X-CSRFToken': csrftoken ?? '',
		...headers,
	};
}

async function refreshJWT() {
	// Access token might be expired, try refreshing it
	const refreshToken = localStorage.getItem('refresh_token');

	const refreshResponse = await ajax('/auth/token/refresh/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ refresh: refreshToken }),
	});

	if (refreshResponse.ok) {
		const data = await refreshResponse.json();
		localStorage.setItem('access_token', data.access);
		localStorage.setItem('refresh_token', data.refresh);
		return true;
	} else {
		console.log('refresh token is invalid');
		// Refresh token is invalid/expired, redirect to login
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		deleteCookie('access_token');
		deleteCookie('refresh_token');
		navigateTo('/');
		return false;
	}
}

window.ajax = ajax;
window.ajaxWithAuth = ajaxWithAuth;
