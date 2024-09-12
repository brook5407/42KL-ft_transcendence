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
