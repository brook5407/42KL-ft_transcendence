import { Paddle } from './classes/paddle.js';
import { Ball } from './classes/ball.js';
import { Table } from './classes/table.js';
import { getWSHost } from '../websocket.js';

const wsHost = getWSHost();

export class GameClient {
	constructor(gameMode, roomId) {
		this.gameMode = gameMode;
		this.roomId = roomId;
		this.assignedPaddle = null;

		this.pongGameContainer = document.getElementById('pong-game-container');
		this.gameCanvas = document.getElementById('gameCanvas');
		this.score1 = document.getElementById('score1');
		this.score2 = document.getElementById('score2');
		this.canvasContainer = document.getElementById('canvasContainer');
		this.overlay = document.getElementById('overlay');
		this.countdownText = document.getElementById('countdownText');
		this.winnerText = document.getElementById('winnerText');
		this.matchmaking = document.getElementById('matchmaking');
		this.roomCode = document.getElementById('roomCode');

		this.roomCode.innerHTML = this.roomId;

		this.socket = new WebSocket(
			`${wsHost}/ws/${this.gameMode}/${this.roomId}/`
		);

		this.socket.onopen = this.onOpen.bind(this);
		this.socket.onerror = this.onError.bind(this);
		this.socket.onclose = this.onClose.bind(this);
		this.socket.onmessage = this.onMessage.bind(this);

		this.keyDownHandler = this.handleKeyDown.bind(this);
		this.keyUpHandler = this.handleKeyUp.bind(this);
		this.attachEventListeners();
	}

	onOpen() {
		console.log('Pong game WebSocket connection established ' + this.roomId);
		this.socket.send(JSON.stringify({ game_mode: this.gameMode }));
	}

	onError(error) {
		console.error('Pong game WebSocket error:', error);
	}

	onClose(event) {
		console.log('Pong game WebSocket connection closed:', event);
	}

	onMessage(e) {
		const data = JSON.parse(e.data);

		switch (data.type) {
			case 'paddle_assignment':
				this.handlePaddleAssignment(data);
				break;
			case 'start_game':
				this.startGame(data);
				break;
			case 'countdown_game':
				this.countdownGame(data);
				break;
			case 'update_game_state':
				this.updateGameState(data);
				break;
			case 'end_game':
				this.endGame(data);
				break;
			default:
				console.error('Unknown message type:', data.type);
		}
	}

	handlePaddleAssignment(data) {
		console.log('paddle_assignment: ' + data.paddle);
		this.assignedPaddle = data.paddle;
	}

	startGame(data) {
		console.log('start_game');
		this.canvasContainer.height = data.gameHeight;
		this.canvasContainer.width = data.gameWidth;
		this.gameCanvas.height = data.gameHeight;
		this.gameCanvas.width = data.gameWidth;
		this.paddle1 = new Paddle(
			data.paddle1.x,
			data.paddle1.y,
			data.paddle1.width,
			data.paddle1.height,
			'white'
		);
		this.paddle2 = new Paddle(
			data.paddle2.x,
			data.paddle2.y,
			data.paddle2.width,
			data.paddle2.height,
			'white'
		);
		this.ball = new Ball(
			this.gameCanvas.width / 2,
			this.gameCanvas.height / 2,
			data.ball.radius,
			data.ball.speed,
			'#ffffff',
			'#A0D8F0'
		);
		this.table = new Table(
			this.gameCanvas,
			this.paddle1,
			this.paddle2,
			this.ball
		);
		this.matchmaking.style.display = 'none';
		this.pongGameContainer.style.display = 'flex';
		if (this.assignedPaddle === 'paddle1') {
			this.paddle1.color = '#4FCDF0';
			this.score1.style.color = '#4FCDF0';
			this.paddle2.color = '#EC4242';
			this.score2.style.color = '#EC4242';
		} else if (this.assignedPaddle === 'paddle2') {
			this.paddle1.color = '#EC4242';
			this.score1.style.color = '#EC4242';
			this.paddle2.color = '#4FCDF0';
			this.score2.style.color = '#4FCDF0';
		}
	}

	countdownGame(data) {
		console.log('countdown_game');
		const countdownValue = data.message;
		this.countdownText.style.display = 'block';
		this.countdownText.innerHTML = countdownValue;

		if (countdownValue === 1) {
			setTimeout(() => {
				this.countdownText.innerHTML = 'Go!';
			}, 1000);
			setTimeout(() => {
				this.countdownText.style.display = 'none';
				this.overlay.style.display = 'none';
			}, 2000);
		}
		this.table.draw();
	}

	updateGameState(data) {
		console.log('update_game_state');
		this.paddle1.y = data.paddle1.y;
		this.paddle2.y = data.paddle2.y;
		this.ball.x = data.ball.x;
		this.ball.y = data.ball.y;
		this.score1.innerText = data.score1;
		this.score2.innerText = data.score2;

		this.table.draw();
	}

	endGame(data) {
		console.log('end_game');
		this.overlay.style.display = 'flex';
		this.winnerText.style.display = 'flex';
		this.winnerText.innerText = data.message;

		let countdown = 11;
		const countdownInterval = setInterval(() => {
			countdown -= 1;
			this.countdownText.style.fontSize = '12px';
			this.countdownText.innerText = `Returning to the main menu in ${countdown} seconds...`;
			this.countdownText.style.display = 'flex';

			if (countdown === 0) {
				clearInterval(countdownInterval);
				navigateTo('/');
			}
		}, 1000);
	}

	attachEventListeners() {
		document.addEventListener('keydown', this.keyDownHandler);
		document.addEventListener('keyup', this.keyUpHandler);
	}

	detachEventListeners() {
		document.removeEventListener('keydown', this.keyDownHandler);
		document.removeEventListener('keyup', this.keyUpHandler);
	}

	handleKeyDown(event) {
		let movement = null;

		if (event.key === 'w') {
			movement = 'up';
		} else if (event.key === 's') {
			movement = 'down';
		}

		if (movement !== null) {
			this.socket.send(
				JSON.stringify({ paddle: this.assignedPaddle, movement: movement })
			);
		}
	}

	handleKeyUp(event) {
		if (event.key === 'w' || event.key === 's') {
			this.socket.send(
				JSON.stringify({ paddle: this.assignedPaddle, movement: 'stop' })
			);
		}
	}

	destroy() {
		this.detachEventListeners();
		this.socket.close();
	}
}

export class TournamentClient {
	constructor(tourenamentId) {
		this.socket = null;
		this.tourenamentId = tourenamentId;
		this.assignedPaddle = null;

		this.pongGameContainer = document.getElementById('pong-game-container');
		this.gameCanvas = document.getElementById('gameCanvas');
		this.score1 = document.getElementById('score1');
		this.score2 = document.getElementById('score2');
		this.canvasContainer = document.getElementById('canvasContainer');
		this.overlay = document.getElementById('overlay');
		this.countdownText = document.getElementById('countdownText');
		this.winnerText = document.getElementById('winnerText');
		this.matchmaking = document.getElementById('matchmaking');

		this.keyDownHandler = this.handleKeyDown.bind(this);
		this.keyUpHandler = this.handleKeyUp.bind(this);
		this.attachEventListeners();
	}

	onMessage(e) {
		const data = JSON.parse(e.data);

		switch (data.type) {
			case 'paddle_assignment':
				this.handlePaddleAssignment(data);
				break;
			case 'start_game':
				this.startGame(data);
				break;
			case 'countdown_game':
				this.countdownGame(data);
				break;
			case 'update_game_state':
				this.updateGameState(data);
				break;
			case 'end_game':
				this.endGame(data);
				break;
			case 'next_match':
				// this.nextMatch(data);
				break;
			default:
				console.error('Unknown message type:', data.type);
		}
	}

	handlePaddleAssignment(data) {
		console.log('paddle_assignment: ' + data.paddle);
		this.assignedPaddle = data.paddle;
	}

	startGame(data) {
		console.log('start_game');
		this.canvasContainer.height = data.gameHeight;
		this.canvasContainer.width = data.gameWidth;
		this.gameCanvas.height = data.gameHeight;
		this.gameCanvas.width = data.gameWidth;
		this.paddle1 = new Paddle(
			data.paddle1.x,
			data.paddle1.y,
			data.paddle1.width,
			data.paddle1.height,
			'white'
		);
		this.paddle2 = new Paddle(
			data.paddle2.x,
			data.paddle2.y,
			data.paddle2.width,
			data.paddle2.height,
			'white'
		);
		this.ball = new Ball(
			this.gameCanvas.width / 2,
			this.gameCanvas.height / 2,
			data.ball.radius,
			data.ball.speed,
			'#ffffff',
			'#A0D8F0'
		);
		this.table = new Table(
			this.gameCanvas,
			this.paddle1,
			this.paddle2,
			this.ball
		);
		this.matchmaking.style.display = 'none';
		this.pongGameContainer.style.display = 'flex';
		if (this.assignedPaddle === 'paddle1') {
			this.paddle1.color = '#4FCDF0';
			this.score1.style.color = '#4FCDF0';
			this.paddle2.color = '#EC4242';
			this.score2.style.color = '#EC4242';
		} else if (this.assignedPaddle === 'paddle2') {
			this.paddle1.color = '#EC4242';
			this.score1.style.color = '#EC4242';
			this.paddle2.color = '#4FCDF0';
			this.score2.style.color = '#4FCDF0';
		}
	}

	countdownGame(data) {
		console.log('countdown_game');
		const countdownValue = data.message;
		this.countdownText.style.display = 'block';
		this.countdownText.innerHTML = countdownValue;

		if (countdownValue === 1) {
			setTimeout(() => {
				this.countdownText.innerHTML = 'Go!';
			}, 1000);
			setTimeout(() => {
				this.countdownText.style.display = 'none';
				this.overlay.style.display = 'none';
			}, 2000);
		}
		this.table.draw();
	}

	updateGameState(data) {
		console.log('update_game_state');
		this.paddle1.y = data.paddle1.y;
		this.paddle2.y = data.paddle2.y;
		this.ball.x = data.ball.x;
		this.ball.y = data.ball.y;
		this.score1.innerText = data.score1;
		this.score2.innerText = data.score2;

		this.table.draw();
	}

	endGame(data) {
		console.log('end_game');
		this.overlay.style.display = 'flex';
		this.winnerText.style.display = 'flex';
		this.winnerText.innerText = data.message;

		// let countdown = 11;
		// const countdownInterval = setInterval(() => {
		// 	countdown -= 1;
		// 	this.countdownText.style.fontSize = '12px';
		// 	this.countdownText.innerText = `Returning to the main menu in ${countdown} seconds...`;
		// 	this.countdownText.style.display = 'flex';

		// 	if (countdown === 0) {
		// 		clearInterval(countdownInterval);
		// 		navigateTo('/');
		// 	}
		// }, 1000);
	}

	attachEventListeners() {
		document.addEventListener('keydown', this.keyDownHandler);
		document.addEventListener('keyup', this.keyUpHandler);
	}

	detachEventListeners() {
		document.removeEventListener('keydown', this.keyDownHandler);
		document.removeEventListener('keyup', this.keyUpHandler);
	}

	handleKeyDown(event) {
		let movement = null;

		if (event.key === 'w') {
			movement = 'up';
		} else if (event.key === 's') {
			movement = 'down';
		}

		console.log('movement: ' + movement);

		if (movement !== null && this.socket && this.assignedPaddle) {
			this.socket.send(
				JSON.stringify({
					type: 'game_action',
					paddle: this.assignedPaddle,
					movement: movement,
				})
			);
		}
	}

	handleKeyUp(event) {
		if (event.key !== 'w' && event.key !== 's') {
			return;
		}
		if (this.socket && this.assignedPaddle) {
			this.socket.send(
				JSON.stringify({
					type: 'game_action',
					paddle: this.assignedPaddle,
					movement: 'stop',
				})
			);
		}
	}

	destroy() {
		this.detachEventListeners();
	}
}
