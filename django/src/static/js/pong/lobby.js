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
	console.log(roomcode.Length());
	if (roomCode) {
		navigateTo(`/pong/tournament/${roomCode}/`);
	}
	else if (roomCode.Length() != 5) {
		document.getElementById('message').textContent = 'Please enter a valid code';
	}
	else {
		document.getElementById('message').textContent = 'Please enter a room code.';
	}
});