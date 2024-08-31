function getCookie(name) {
	const nameEQ = name + '=';
	const ca = document.cookie.split(';');
	for (let i = 0; i < ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) === ' ') c = c.substring(1, c.length);
		if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
	}
	return null;
}

function setTokensFromCookies() {
	const accessToken = getCookie('access_token');
	const refreshToken = getCookie('refresh_token');

	if (accessToken) {
		localStorage.setItem('access_token', accessToken);
	}
	if (refreshToken) {
		localStorage.setItem('refresh_token', refreshToken);
	}
}

// Call this function after the OAuth2 callback response is received
window.onload = function () {
	setTokensFromCookies();
};
