import { Paddle } from './classes/paddle.js';
import { Ball } from './classes/ball.js';
import { Table } from './classes/table.js';

// Websocket
const socket = new WebSocket(`ws://${window.location.host}/ws/pong/${roomName}/`);

let assignedPaddle = null;

socket.onopen = function() {
    console.log("WebSocket connection established");
};
socket.onerror = function(error) {
    console.error("WebSocket error:", error);
};
socket.onclose = function(event) {
    console.log("WebSocket connection closed:", event);
};
socket.onmessage = function(e) {
    console.log("Raw message data:", e.data);
    const data = JSON.parse(e.data);
    console.log("Parsed data:", data);

    if (data.type) {
        console.log("Message type:", data.type);
    } else {
        console.error("Message type is undefined");
    }

    if (data.type === 'player_assignment') {
        // Store the assigned paddle
        assignedPaddle = data.player;
    }

    if (data.type === 'update_game_state') {
        // Update the game state based on the server's response
        paddle1.y = data.paddle1.y;
        paddle2.y = data.paddle2.y;
        ball.x = data.ball.x;
        ball.y = data.ball.y;

        // Render the updated game state
        table.draw();
    }
};

document.addEventListener('keydown', (event) => {
    let velocity = null;

    if (assignedPaddle === 'paddle1' && (event.key === 'w' || event.key === 's')) {
        velocity = event.key === 'w' ? -5 : 5;
    } else if (assignedPaddle === 'paddle2' && (event.key === 'ArrowUp' || event.key === 'ArrowDown')) {
        velocity = event.key === 'ArrowUp' ? -5 : 5;
    }

    if (velocity !== null) {
        socket.send(JSON.stringify({ 'paddle': assignedPaddle, 'velocity': velocity }));
    }
});

document.addEventListener('keyup', (event) => {
    if (assignedPaddle === 'paddle1' && (event.key === 'w' || event.key === 's') ||
        assignedPaddle === 'paddle2' && (event.key === 'ArrowUp' || event.key === 'ArrowDown')) {
        socket.send(JSON.stringify({ 'paddle': assignedPaddle, 'velocity': 0 }));
    }
});

// Client-side game setup and rendering
const gameCanvas = document.getElementById('gameCanvas');
const paddle1 = new Paddle(5, 200, 10, 100, 'white', 5);
const paddle2 = new Paddle(gameCanvas.width - 15, gameCanvas.height - 300, 10, 100, 'white', 5);
const ball = new Ball(gameCanvas.width / 2, gameCanvas.height / 2, 8, 'lightblue', 'lightblue', 2);
const table = new Table(gameCanvas, paddle1, paddle2, ball);

// Game table object handling the rendering
table.draw = function() {
    this.clearBoard();
    this.paddle1.draw(this.ctx);
    this.paddle2.draw(this.ctx);
    this.ball.draw(this.ctx);
};



// let form = document.getElementById('form')
// form.addEventListener('submit', (e)=> {
//     e.preventDefault()
//     let message = e.target.message.value
//     socket.send(JSON.stringify({
//         'message':message
//     }))
//     form.reset()
// })

// let assignedPaddle = null;

// socket.onmessage = function(e) {
//     const data = JSON.parse(e.data);
//     console.log('Data:', data)

//     if (data.type === 'chat'){
//         let messages = document.getElementById('messages')

//         messages.insertAdjacentHTML('beforeend', `<div>
//                                 <p>${data.message}</p>
//                             </div>`)
//     }

//     if (data.player) {
//         // Assign the paddle to the client
//         assignedPaddle = data.player;
//     } else {
//         const paddle = data['paddle'];
//         const velocity = data['velocity'];

//         if (paddle === 'paddle1') {
//             paddle1.velocity = velocity;
//         } else if (paddle === 'paddle2') {
//             paddle2.velocity = velocity;
//         }
//     }
// };

// document.addEventListener('keydown', (event) => {
//     if (!assignedPaddle) return;

//     let velocity = null;

//     if (assignedPaddle === 'paddle1' && (event.key === 'w' || event.key === 's')) {
//         velocity = event.key === 'w' ? -paddle1.speed : paddle1.speed;
//     } else if (assignedPaddle === 'paddle2' && (event.key === 'ArrowUp' || event.key === 'ArrowDown')) {
//         velocity = event.key === 'ArrowUp' ? -paddle2.speed : paddle2.speed;
//     }

//     if (velocity !== null) {
//         socket.send(JSON.stringify({ 'paddle': assignedPaddle, 'velocity': velocity }));
//     }
// });

// document.addEventListener('keyup', (event) => {
//     if (!assignedPaddle) return;

//     if ((assignedPaddle === 'paddle1' && (event.key === 'w' || event.key === 's')) ||
//         (assignedPaddle === 'paddle2' && (event.key === 'ArrowUp' || event.key === 'ArrowDown'))) {
//         socket.send(JSON.stringify({ 'paddle': assignedPaddle, 'velocity': 0 }));
//     }
// });

// table.gameLoop();
// table.startCountdown();

// resetButton.addEventListener('click', () => table.resetGame());
// pauseButton.addEventListener('click', () => table.togglePause());
// gameCanvas.addEventListener('click', () => table.togglePause());



// document.addEventListener('keydown', (event) => {
// 	switch (event.key) {
// 		case 'Escape':
// 			table.togglePause();
// 			break;
// 		case 'w':
// 			paddle1.velocity = -paddle1.speed;
// 			break;
// 		case 's':
// 			paddle1.velocity = paddle1.speed;
// 			break;
// 		case 'ArrowUp':
// 			paddle2.velocity = -paddle2.speed;
// 			break;
// 		case 'ArrowDown':
// 			paddle2.velocity = paddle2.speed;
// 			break;
// 	}
// });

// document.addEventListener('keyup', (event) => {
// 	if (event.key === 'w' || event.key === 's') paddle1.velocity = 0;
// 	else if (event.key === 'ArrowUp' || event.key === 'ArrowDown') paddle2.velocity = 0;
// });

// first version ~~
// const gameCanvas = document.querySelector('#gameCanvas');
// const ctx = gameCanvas.getContext('2d');
// const scoreText = document.querySelector('#scoreBoard');
// const resetButton = document.querySelector('#resetButton');
// const pauseButton = document.querySelector('#pauseButton');
// const gameHeight = gameCanvas.height;
// const gameWidth = gameCanvas.width;
// const boardBackground = 'black';
// let pause = true;
// let animationID;

// const paddle = {
// 	color1: 'white',
// 	color2: 'white',
// 	border: 'white',
// 	speed: 5,
// };

// let ball = {
// 	color: 'white',
// 	borderColor: 'white',
// 	radius: 8,
// 	speed: 1,
// 	x: gameWidth / 2,
// 	y: gameHeight / 2,
// 	xDirection: 0,
// 	yDirection: 0,
// };

// let intervalID;
// let player1Score = 0;
// let player2Score = 0;

// let paddle1 = {
// 	width: 10,
// 	height: 100,
// 	x: 5,
// 	y: 200,
// 	velocity: 0,
// };

// let paddle2 = {
// 	width: 10,
// 	height: 100,
// 	x: gameWidth - 15,
// 	y: gameHeight - 300,
// 	velocity: 0,
// };

// document.addEventListener('keydown', (event) => {
// 	// console.log(keyPressed);
// 	switch (event.key) {
// 		case 'Escape':
// 			togglePause();
// 			break;
// 		default:
// 			pause = false;
// 			break;
// 	}

// 	if (!pause) {
// 		if (event.key === 'w') paddle1.velocity = -paddle.speed;
// 		else if (event.key === 's') paddle1.velocity = paddle.speed;
// 		else if (event.key === 'ArrowUp') paddle2.velocity = -paddle.speed;
// 		else if (event.key === 'ArrowDown') paddle2.velocity = paddle.speed;
// 	}
// });

// document.addEventListener('keyup', (event) => {
// 	if (event.key === 'w' || event.key === 's') paddle1.velocity = 0;
// 	else if (event.key === 'ArrowUp' || event.key === 'ArrowDown')
// 		paddle2.velocity = 0;
// });

// resetButton.addEventListener('click', resetGame);
// pauseButton.addEventListener('click', togglePause);
// gameCanvas.addEventListener('click', togglePause);

// const gameModeSelect = document.getElementById('gameMode');
// const difficultySelect = document.getElementById('difficulty');
// let difficultySpeed = 0;

// gameModeSelect.addEventListener('change', function () {
// 	if (gameModeSelect.value == 'Player') {
// 		// difficultySelect.style.display = 'none'; // Hide difficulty select
// 		resetGame();
// 		cancelAnimationFrame(animationID);
// 		// console.log(gameModeSelect.value);
// 		gameLoop();
// 	} else if (gameModeSelect.value === 'Computer') {
// 		// difficultySelect.style.display = 'inline'; // Show difficulty select
// 		resetGame();
// 		cancelAnimationFrame(animationID);
// 		// console.log(gameModeSelect.value);
// 		gameLoop();
// 	}
// });

// gameStart();

// function gameStart() {
// 	createBall();
// 	gameLoop();
// }

// function togglePause() {
// 	pause = !pause;
// }

// function pauseOverlay() {
// 	const midX = gameWidth / 2;
// 	const midY = gameHeight / 2;
// 	if (pause == true) {
// 		ctx.fillStyle = '#222222';
// 		ctx.fillRect(0, 0, gameWidth, gameHeight);

// 		ctx.fillStyle = '#FFFFFF75';
// 		ctx.arc(midX, midY, 50, 0, 2 * Math.PI);
// 		ctx.fill();
// 		ctx.fillRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);
// 		ctx.fillRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height);

// 		ctx.fillStyle = '#323232';
// 		ctx.fillRect(midX - 5, midY - 20, -10, 40);
// 		ctx.fillRect(midX + 5, midY - 20, 10, 40);

// 		ctx.fillStyle = '#FFFFFF75';
// 		ctx.font = '20px sans-serif';
// 		ctx.textAlign = 'center';
// 		ctx.fillText('Press the screen or any key to continue', midX, midY + 100);
// 	}
// }

// function updateAIPaddle() {
// 	const paddleCenter = paddle2.y + paddle2.height / 2;

// 	if (ball.y > paddleCenter) paddle2.velocity = ball.speed;
// 	else if (ball.y < paddleCenter) paddle2.velocity = -ball.speed;
// 	else paddle2.velocity = 0;
// }

// function gameLoop() {
// 	clearBoard();
// 	drawPaddles();
// 	update();
// 	drawBall(ball.x, ball.y);
// 	checkCollision();
// 	if (gameModeSelect.value == 'Computer') {
// 		updateAIPaddle();
// 	}
// 	updateScore();
// 	pauseOverlay();
// 	animationID = requestAnimationFrame(gameLoop);
// }

// function clearBoard() {
// 	ctx.fillStyle = boardBackground;
// 	ctx.fillRect(0, 0, gameWidth, gameHeight);
// }

// function drawPaddles() {
// 	ctx.strokeStyle = paddle.border;

// 	ctx.fillStyle = paddle.color1;
// 	ctx.fillRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);
// 	ctx.strokeRect(paddle1.x, paddle1.y, paddle1.width, paddle1.height);

// 	ctx.fillStyle = paddle.color2;
// 	ctx.fillRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height);
// 	ctx.strokeRect(paddle2.x, paddle2.y, paddle2.width, paddle2.height);
// }

// function createBall() {
// 	ball.speed = 2;
// 	if (Math.round(Math.random()) == 1) ball.xDirection = 1;
// 	else ball.xDirection = -1;
// 	if (Math.round(Math.random()) == 1) ball.yDirection = 1;
// 	else ball.yDirection = -1;
// 	ball.x = gameWidth / 2;
// 	ball.y = gameHeight / 2;
// 	drawBall(ball.x, ball.y);
// }

// function update() {
// 	if (pause == false) {
// 		ball.x += ball.speed * ball.xDirection;
// 		ball.y += ball.speed * ball.yDirection;
// 	}
// 	paddle1.y += paddle1.velocity;
// 	paddle2.y += paddle2.velocity;

// 	if (paddle1.y < 0) paddle1.y = 0;
// 	if (paddle1.y > gameHeight - paddle1.height)
// 		paddle1.y = gameHeight - paddle1.height;
// 	if (paddle2.y < 0) paddle2.y = 0;
// 	if (paddle2.y > gameHeight - paddle2.height)
// 		paddle2.y = gameHeight - paddle1.height;
// }

// function drawBall(x, y) {
// 	ctx.fillStyle = ball.color;
// 	ctx.strokeStyle = ball.borderColor;
// 	ctx.lineWidth = 2;
// 	ctx.beginPath();
// 	ctx.arc(ball.x, ball.y, ball.radius, 0, 2 * Math.PI);
// 	ctx.stroke();
// 	ctx.fill();
// }

// function checkCollision() {
// 	if (ball.y <= 0 + ball.radius) ball.yDirection *= -1;
// 	if (ball.y >= gameHeight - ball.radius) ball.yDirection *= -1;
// 	if (ball.x <= 0) {
// 		player2Score += 1;
// 		createBall();
// 		return;
// 	}
// 	if (ball.x >= gameWidth) {
// 		player1Score += 1;
// 		createBall();
// 		return;
// 	}
// 	if (ball.x <= paddle1.x + paddle1.width + ball.radius) {
// 		if (ball.y > paddle1.y && ball.y < paddle1.y + paddle1.height) {
// 			ball.x = paddle1.x + paddle1.width + ball.radius; // if ball gets stuck
// 			ball.xDirection *= -1;
// 			ball.speed += 0.5;
// 		}
// 	}
// 	if (ball.x >= paddle2.x - ball.radius) {
// 		if (ball.y > paddle2.y && ball.y < paddle2.y + paddle2.height) {
// 			ball.x = paddle2.x - ball.radius; // if ball gets stuck
// 			ball.xDirection *= -1;
// 			ball.speed += 0.5;
// 		}
// 	}
// 	// console.log(ball.speed);
// }

// function updateScore() {
// 	scoreText.textContent = `${player1Score} : ${player2Score}`;
// 	if (player1Score == 5) {
// 		alert('Left Player Wins!');
// 		resetGame();
// 	} else if (player2Score == 5) {
// 		alert('Right Player Wins!');
// 		resetGame();
// 	}
// }

// function resetGame() {
// 	player1Score = 0;
// 	player2Score = 0;
// 	paddle1.y = 200;
// 	paddle2.y = 200;
// 	ball.speed = 3;
// 	paddle1.velocity = 0;
// 	paddle2.velocity = 0;
// 	ball.x = gameWidth / 2;
// 	ball.y = gameHeight / 2;
// 	pause = true;
// 	updateScore();
// 	createBall();
// }
