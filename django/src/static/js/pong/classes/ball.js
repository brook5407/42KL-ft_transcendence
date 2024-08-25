export class Ball {
	constructor(x, y, radius, speed, color, borderColor) {
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.speed = speed;
		this.color = color;
		this.borderColor = borderColor;
		this.xDirection = 0;
		this.yDirection = 0;
	}

	draw(ctx) {
		ctx.fillStyle = this.color;
		ctx.strokeStyle = this.borderColor;
		ctx.lineWidth = 2;
		ctx.beginPath();
		ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
		ctx.stroke();
		ctx.fill();
	}

	move() {
		this.x += this.speed * this.xDirection;
		this.y += this.speed * this.yDirection;
	}

	checkCollision(gameHeight, paddle1, paddle2) {
		if (this.y <= 0 + this.radius || this.y >= gameHeight - this.radius)
			this.yDirection *= -1;

		if (
			this.x <= paddle1.x + paddle1.width + this.radius &&
			this.y > paddle1.y &&
			this.y < paddle1.y + paddle1.height
		) {
			this.xDirection *= -1;
			this.speed += 0.5;
		}

		if (
			this.x >= paddle2.x - this.radius &&
			this.y > paddle2.y &&
			this.y < paddle2.y + paddle2.height
		) {
			this.xDirection *= -1;
			this.speed += 0.5;
		}
	}

	reset(gameWidth, gameHeight) {
		this.x = gameWidth / 2;
		this.y = gameHeight / 2;
		this.speed = 2;
		this.xDirection = Math.round(Math.random()) === 1 ? 1 : -1;
		this.yDirection = Math.round(Math.random()) === 1 ? 1 : -1;
	}
}