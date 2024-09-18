import { navigateTo, router } from './navigation.js';

export function ajax(url, options) {
	options.headers = constructRequestHeader(options.headers);

	const fetchOptions = Object.assign(
		{
			method: 'POST',
			credentials: 'include',
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

export async function ajaxWithAuth(
	url,
	options,
	needRefreshJWT = true,
	retries = 0
) {
	options.headers = constructRequestHeader(options.headers);

	const fetchOptions = Object.assign(
		{
			method: 'POST',
			credentials: 'include',
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
	if (response.status === 401 && needRefreshJWT) {
		if (retries >= 2) {
			// Redirect to login page
			navigateTo('/');
			return response;
		}
		const status = await refreshJWT();
		if (!status) return response;
		// Retry the original request with new access token
		const retryResponse = await ajaxWithAuth(url, options, true, retries + 1);
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

export async function refreshJWT() {
	const refreshResponse = await ajax('/auth/token/refresh/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		credentials: 'include',
	});

	return refreshResponse.ok;
}

window.ajax = ajax;
window.ajaxWithAuth = ajaxWithAuth;
