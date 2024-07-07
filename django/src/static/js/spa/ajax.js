export function ajax(url, options) {
	const fetchOptions = Object.assign(
		{
			method: 'POST',
			credentials: 'same-origin',
			headers: {
				'X-Requested-With': 'XMLHttpRequest',
			},
		},
		options
	);

	return fetch(url, fetchOptions);
}
