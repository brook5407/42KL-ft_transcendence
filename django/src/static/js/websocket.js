function getWSHost() {
	const host = window.location.host;
	const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	return `${protocol}//${host}`;
}

window.getWSHost = getWSHost;
