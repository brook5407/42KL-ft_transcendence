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
        // Create radial gradient for ice effect
        let gradient = ctx.createRadialGradient(this.x, this.y, this.radius * 0.3, this.x, this.y, this.radius);
        gradient.addColorStop(0, "#E0F7FF");  // Light icy blue
        gradient.addColorStop(1, "#A0D8F0");  // Slightly darker icy blue

        // Apply the ice gradient color to the ball
        ctx.fillStyle = gradient;
        
        // Apply shadow for glowing effect
        ctx.shadowBlur = 15;
        ctx.shadowColor = 'rgba(173, 216, 230, 0.8)';  // Ice glow color
        
        // Ball border
        ctx.strokeStyle = this.borderColor;
        ctx.lineWidth = 2;

        // Draw the ball
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
        ctx.stroke();  // Border stroke
        ctx.fill();    // Fill ball with gradient
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