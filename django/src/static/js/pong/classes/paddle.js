export class Paddle {
	constructor(x, y, width, height, color, speed) {
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
		this.color = color;
		this.speed = speed;
		this.velocity = 0;
	}

	draw(ctx) {
		ctx.fillStyle = this.color;
		ctx.fillRect(this.x, this.y, this.width, this.height);
	}

	move() {
		this.y += this.velocity;
	}

	checkBounds(gameHeight) {
		if (this.y < 0) this.y = 0;
		if (this.y > gameHeight - this.height) this.y = gameHeight - this.height;
	}

	reset() {
		this.velocity = 0;
		this.y = 200;
	}
}