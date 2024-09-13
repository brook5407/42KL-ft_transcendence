import { Paddle } from './classes/paddle.js';
import { Ball } from './classes/ball.js';
import { Table } from './classes/table.js';

// const roomNameElement = document.getElementById('room-name');
// const roomName = JSON.parse(roomNameElement.textContent);

const hitSound = new Audio('/static/audio/hit.mp3');
const scoreSound = new Audio('/static/audio/score.mp3');
hitSound.load();
scoreSound.load();
function playHitSound() {
    hitSound.play();
}

function playScoreSound() {
    scoreSound.play();
}

window.config = {
	roomCode: null,
	socket: null
};

document.getElementById('create-room').addEventListener('click', function() {
	fetch('/pong/tournament/create')
		.then(response => response.json())
		.then(data => {
			if (data.room_name) {
				// window.config = {
				// 	roomCode: data.room_name
				// };
				window.config.roomCode = data.room_name;
			}
			navigateTo(data.redirect_url);
		})
		.catch(error => console.error('Error creating room:', error));
	roomDisplay.innerHTML = window.config.roomCode;
	// if (window.config.roomCode) {
	// 	window.config.socket = new WebSocket(`ws://${window.location.host}/ws/tournament/${gameMode}/${window.config.roomCode}/`);
	// }
	// window.config.socket = new WebSocket(`ws://${window.location.host}/ws/tournament/${gameMode}/${window.config.roomCode}/`);
});

document.getElementById('join-room').addEventListener('click', function() {
	const roomName = document.getElementById('room-code').value;
	console.log(roomName.length);
	if (roomName) {
		// window.config = {
		// 	roomCode: document.getElementById('room-code').value
		// };
		window.config.roomCode = document.getElementById('room-code').value;
		navigateTo(`/pong/tournament/${roomName}/`);
	}
	else if (roomName.length != 5) {
		document.getElementById('message').textContent = 'Please enter a valid code';
	}
	else {
		document.getElementById('message').textContent = 'Please enter a room code.';
	}
	roomDisplay.innerHTML = window.config.roomCode;
	// if (window.config.roomCode) {
	// 	window.config.socket = new WebSocket(`ws://${window.location.host}/ws/tournament/${gameMode}/${window.config.roomCode}/`);
	// }
	// window.config.socket = new WebSocket(`ws://${window.location.host}/ws/tournament/${gameMode}/${window.config.roomCode}/`);
});


// const socket = new WebSocket(`ws://${window.location.host}/ws/tournament/${gameMode}/${window.config.roomCode}/`);
const socket = window.config.socket;
// roomDisplay.innerHTML = window.config.roomCode;
const roomName = window.config.roomCode;



// // ----------------- Game logic -----------------------------------------------------------------------------------------------//
// //Follow main.js for game logic


// socket.onopen = function() {
//     console.log("WebSocket connection established " + roomName);
//     socket.send(JSON.stringify({ 'game_mode': gameMode}));
// };
// socket.onerror = function(error) {
//     console.error("WebSocket error:", error);
// };
// socket.onclose = function(event) {
//     console.log("WebSocket connection closed:", event);
// };
// socket.onmessage = function(e) {
//     const data = JSON.parse(e.data);
//     // console.log("Raw message data:", e.data);
//     // console.log("Parsed data:", data);
//     // if (data.type) {
//     //     console.log("Message type:", data.type);
//     // } else {
//     //     console.error("Message type is undefined");
//     // }

//     if (data.type === 'player_assignment') {
//         // Store the assigned paddle
//         console.log("player_assignment");
//         assignedPaddle = data.player;
//     }
//     if (data.type === 'start_game') {
//         // Both players has connected, start the game
//         console.log("start_game");
//         canvasContainer.height = data.gameHeight;
//         canvasContainer.width = data.gameWidth;
//         gameCanvas.height = data.gameHeight;
//         gameCanvas.width = data.gameWidth;
//         paddle1 = new Paddle(data.paddle1.x, data.paddle1.y, data.paddle1.width, data.paddle1.height, 'white');
//         // if (ball.y > paddle1.y && ball.y < paddle1.y + paddle1.height)
// 		// 	playHitSound();
//         paddle2 = new Paddle(data.paddle2.x, data.paddle2.y, data.paddle2.width, data.paddle2.height, 'white');
//         // if (ball.y > paddle2.y && ball.y < paddle2.y + paddle2.height)
// 		// 	playHitSound();
//         ball = new Ball(gameCanvas.width / 2, gameCanvas.height / 2, data.ball.radius, data.ball.speed, 'lightblue', 'lightblue');
//         // if (ball.x <= (paddle1.x + paddle1.width + ball.radius)) {
//         //     // if (ball.y > paddle1.y && ball.y < paddle1.y + paddle1.height)
//         //         playHitSound();
//         // }
//         // if (ball.x >= (paddle2.x - ball.radius)) {
//         //     // if (ball.y > paddle2.y && ball.y < paddle2.y + paddle2.height)
//         //         playHitSound();
//         // }
//         table = new Table(gameCanvas, paddle1, paddle2, ball);
//         matchmaking.style.display = 'none';
//         gameCanvas.style.display = 'block';
//         scoreBoard.style.display = 'block';
//         if (assignedPaddle === 'paddle1') {
//             paddle1.color = "lightgreen";
//         } else if (assignedPaddle === 'paddle2') {
//             paddle2.color = "lightgreen";
//         }
//     }
//     if (data.type === 'countdown_game') {
//         console.log("countdown_game");
//         const countdownValue = data.message;
//         countdownText.style.display = 'block';
//         countdownText.innerHTML = countdownValue;

//         if (countdownValue === 1) {
//             setTimeout(() => {
//                 countdownText.innerHTML = 'Go!';
//             }, 1000);  
//             setTimeout(() => {
//                 countdownText.style.display = 'none';
//                 overlay.style.display = 'none';
//             }, 2000);
//         }
//         table.draw();
//     }
//     if (data.type === 'update_game_state') {
//         console.log("update_game_state");
//         // Update the game state based on the server's response
//         paddle1.y = data.paddle1.y;
//         paddle2.y = data.paddle2.y;
//         ball.x = data.ball.x;
//         ball.y = data.ball.y;
//         // if (ball.y <= 0) {
//             //     playScoreSound();
//             // } 
//         if (ball.x <= 0) {
//             playScoreSound();
//         } 
//         console.log("gameCanvas.width:", gameCanvas.width);
//         if (ball.x >= gameCanvas.width) {
//             playScoreSound();
//         }  
//         document.getElementById('score1').innerText = data.score1;
//         document.getElementById('score2').innerText = data.score2;
//         if (ball.x <= (paddle1.x + paddle1.width + ball.radius)) {
//             if (ball.y > paddle1.y && ball.y < paddle1.y + paddle1.height)
//                 playHitSound();
//         }
//         if (ball.x >= (paddle2.x - ball.radius)) {
//             if (ball.y > paddle2.y && ball.y < paddle2.y + paddle2.height)
//                 playHitSound();
//         }

//         // Render the updated game state
//         table.draw();
//     }
//     if (data.type === 'end_game') {
//         console.log("end_game");
//         alert(data.message);
//         window.location.href = `http://${window.location.host}/`;
//     }
// };


// // Client Paddle Controls
// document.addEventListener('keydown', (event) => {
//     let velocity = null;

//     if (event.key === 'w') {
//         velocity = -10;
//     } else if (event.key === 's') {
//         velocity = 10;
//     }

//     if (velocity !== null) {
//         socket.send(JSON.stringify({ 'paddle': assignedPaddle, 'velocity': velocity }));
//     }
// });

// document.addEventListener('keyup', (event) => {
//     if (event.key === 'w' || event.key === 's') {
//         socket.send(JSON.stringify({ 'paddle': assignedPaddle, 'velocity': 0 }));
//     }
// });



// // let form = document.getElementById('form')
// // form.addEventListener('submit', (e)=> {
// //     e.preventDefault()
// //     let message = e.target.message.value
// //     socket.send(JSON.stringify({
// //         'message':message
// //     }))
// //     form.reset()
// // })

// // socket.onmessage = function(e) {
// //     const data = JSON.parse(e.data);
// //     console.log('Data:', data)

// //     if (data.type === 'chat'){
// //         let messages = document.getElementById('messages')

// //         messages.insertAdjacentHTML('beforeend', `<div>
// //                                 <p>${data.message}</p>
// //                             </div>`)
// //     }



