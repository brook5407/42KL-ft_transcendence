import { navigateTo, router } from './navigation.js';

export function ajax(url, options) {
	const csrftoken = document.cookie
		.split('; ')
		?.find((row) => row.startsWith('csrftoken='))
		?.split('=')[1];

	options.headers = {
		'X-Requested-With': 'XMLHttpRequest',
		'X-CSRFToken': csrftoken ?? '',
		...options.headers,
	};

	const fetchOptions = Object.assign(
		{
			method: 'POST',
			credentials: 'same-origin',
		},
		options
	);

	return fetch(url, fetchOptions);
}

export async function ajax_with_auth(url, options) {
	const csrftoken = document.cookie
		.split('; ')
		?.find((row) => row.startsWith('csrftoken='))
		?.split('=')[1];

	const accessToken = localStorage.getItem('access_token');

	options.headers = {
		'X-Requested-With': 'XMLHttpRequest',
		'X-CSRFToken': csrftoken ?? '',
		...options.headers,
	};

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

	const response = await fetch(url, fetchOptions);
	if (response.status === 401) {
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

			// Retry the original request with new access token
			const retryResponse = await ajax_with_auth(url, {
				...options,
				headers: {
					...options.headers,
					Authorization: `Bearer ${data.access}`,
				},
			});
			return retryResponse;
		} else {
			// Refresh token is invalid/expired, redirect to login
			navigateTo('/');
			openModal('signin');
		}
	}

	return response;
}
