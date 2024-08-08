let socket = new WebSocket('ws://' + window.location.host + '/ws/pong/');

// TODO: make this into OOP

socket.onopen = function (e) {
	console.log('[open] Connection established');
};

socket.onmessage = function (event) {
	let data = JSON.parse(event.data);
	// Update the game state
	console.log('[message] Data received from server: ', data);
	updateGameState(data);
};

socket.onclose = function (event) {
	if (event.wasClean) {
		console.log(
			`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`
		);
	} else {
		console.log('[close] Connection died');
	}
};

socket.onerror = function (error) {
	console.error(`[error] ${error.message}`);
};

function sendGameState(data) {
	socket.send(JSON.stringify(data));
}

function updateGameState(data) {
	// Implement this function to update the game state on the frontend
}
