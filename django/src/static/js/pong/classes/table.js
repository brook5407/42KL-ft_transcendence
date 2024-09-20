// class PongTable {
// 	constructor() {
// 		// calculate the width and height of the table from the window size
// 		this.width = window.innerWidth * 0.7;
// 		this.height = window.innerHeight * 0.7;
// 		this.table = document.createElement('canvas');
// 		this.table.width = this.width;
// 		this.table.height = this.height;
// 		this.context = this.table.getContext('2d');
// 	}
// }
import { Paddle } from './paddle.js';
import { Ball } from './ball.js';

export class Table {
	constructor(canvas, paddle1, paddle2, ball) {
		this.canvas = canvas;
		this.ctx = canvas.getContext('2d');
		this.scoreText = document.querySelector('#scoreBoard');
		this.gameWidth = canvas.width;
		this.gameHeight = canvas.height;
		this.paddle1 = paddle1;
		this.paddle2 = paddle2;
		this.ball = ball;
		this.player1Score = 0;
		this.player2Score = 0;

        this.overlayActive = true;
        this.countdownValue = 3;
	}

	clearBoard() {
		this.ctx.fillStyle = '#BEFAFA';
		this.ctx.fillRect(0, 0, this.gameWidth, this.gameHeight);
	}

	draw() {
		this.clearBoard();
		this.paddle1.draw(this.ctx);
		this.paddle2.draw(this.ctx);
		this.ball.draw(this.ctx);
	}

	update() {
		this.ball.move();
		this.paddle1.move();
		this.paddle2.move();
		this.ball.checkCollision(this.gameHeight, this.paddle1, this.paddle2);
		this.paddle1.checkBounds(this.gameHeight);
		this.paddle2.checkBounds(this.gameHeight);
		this.checkScore();
		this.draw();

		if (this.overlayActive)
			this.drawOverlay();
	}

	checkScore() {
		if (this.ball.x <= 0) {
			this.player2Score++;
			this.ball.reset(this.gameWidth, this.gameHeight);
		} else if (this.ball.x >= this.gameWidth) {
			this.player1Score++;
			this.ball.reset(this.gameWidth, this.gameHeight);
		}

		this.scoreText.textContent = `${this.player1Score} : ${this.player2Score}`;

		let pointsToWin = 999;
		if (this.player1Score === pointsToWin) {
			alert('Left Player Wins!');
			this.resetGame();
		} else if (this.player2Score === pointsToWin) {
			alert('Right Player Wins!');
			this.resetGame();
		}
	}

	resetScore() {
		this.player1Score = 0;
		this.player2Score = 0;
		this.scoreText.textContent = `${this.player1Score} : ${this.player2Score}`;
	}
	
	resetGame() {
		this.resetScore();
		this.paddle1.reset();
		this.paddle2.reset();
		this.ball.reset(this.gameWidth, this.gameHeight);
	}

	startCountdown() {
		this.overlayActive = true;
		const countdownInterval = setInterval(() => {
			if (this.countdownValue > 0) {
				this.countdownValue--;
			} else {
				clearInterval(countdownInterval);
				this.overlayActive = false;
				this.countdownValue = 3; // Reset for future starts
				this.resetGame();
			}
		}, 1000);
	}

	drawOverlay() {
		this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)'; // Semi-dark overlay
		this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

		this.ctx.fillStyle = 'white';
		this.ctx.font = '48px sans-serif';
		this.ctx.textAlign = 'center';
		this.ctx.fillText(this.countdownValue > 0 ? this.countdownValue : 'GO!', this.canvas.width / 2, this.canvas.height / 2);
	}

	gameLoop() {
		this.update();
		requestAnimationFrame(this.gameLoop.bind(this));
	}

	updateAIPaddle() {
		const paddleCenter = this.paddle2.y + this.paddle2.height / 2;
		if (this.ball.y > paddleCenter) this.paddle2.velocity = this.ball.speed;
		else if (this.ball.y < paddleCenter) this.paddle2.velocity = -this.ball.speed;
		else this.paddle2.velocity = 0;
	}
}