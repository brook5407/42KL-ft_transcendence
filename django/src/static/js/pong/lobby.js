document.getElementById('create-room').addEventListener('click', function() {
	fetch('/pong/tournament/create')
		.then(response => response.json())
		.then(data => {
			navigateTo(data.redirect_url);
		})
		.catch(error => console.error('Error creating room:', error));
});

document.getElementById('join-room').addEventListener('click', function() {
	const roomCode = document.getElementById('room-code').value;
	if (roomCode) {
		navigateTo(`/pong/tournament/${roomCode}/`);
	} else {
		document.getElementById('message').textContent = 'Please enter a room code.';
	}
});