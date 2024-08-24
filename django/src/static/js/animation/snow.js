export class Snowfall {
	constructor() {
		this.intervalId = null;

		this.snowflakeImage = new Image();
		this.snowflakeImage.src = '/static/images/snowflake.svg';
		this.snowflakeImage.alt = 'Snowflake';

		this.snowfallInterval = 100; // Milliseconds
		this.frameTimes = [];
		this.maxFrameTimes = 60;

		// adjust snowfall intensity based on frame rate every second
		setInterval(this.measureFrameRate.bind(this), 1000);
	}

	measureFrameRate() {
		let lastFrameTime = performance.now();

		const frame = () => {
			const now = performance.now();
			const delta = now - lastFrameTime;
			lastFrameTime = now;

			this.frameTimes.push(delta);
			if (this.frameTimes.length > this.maxFrameTimes) {
				this.frameTimes.shift();
			}

			const averageFrameTime =
				this.frameTimes.reduce((a, b) => a + b, 0) / this.frameTimes.length;
			const fps = 1000 / averageFrameTime;

			this.adjustSnowfallIntensity(fps);
		};

		requestAnimationFrame(frame);
	}

	adjustSnowfallIntensity(fps) {
		if (fps < 100) {
			this.snowfallInterval = Math.min(this.snowfallInterval + 10, 1000); // Increase interval to reduce snowfall
		} else if (fps > 150) {
			this.snowfallInterval = Math.max(this.snowfallInterval - 10, 100); // Decrease interval to increase snowfall
		}

		if (this.intervalId !== null) {
			clearInterval(this.intervalId);
			this.intervalId = setInterval(
				this.createSnowflake.bind(this),
				this.snowfallInterval
			);
		}
	}

	startSnowfall() {
		if (this.intervalId === null) {
			this.intervalId = setInterval(
				this.createSnowflake.bind(this),
				this.snowfallInterval
			);
		}
	}

	createSnowflake() {
		const randomSeed = Math.random();
		const snowflake = this.snowflakeImage.cloneNode(true);

		snowflake.classList.add('snowflake');
		snowflake.style.left = Math.random() * 100 + 'vw';
		snowflake.style.animationDelay = '0s';
		snowflake.style.animationDuration = Math.random() * 3 + 2 + 's'; // Between 2 and 5 seconds
		snowflake.style.animationName =
			'fall, ' +
			(Math.random() > 0.5 ? 'spin-clockwise' : 'spin-anticlockwise');
		snowflake.style.opacity = randomSeed;
		snowflake.style.width = snowflake.style.height =
			randomSeed * 30 + 10 + 'px';
		snowflake.style.zIndex = Math.min(Math.floor(randomSeed * 100), 1000);

		document.body.appendChild(snowflake);

		// Remove snowflake after it falls
		setTimeout(() => {
			snowflake.remove();
		}, parseInt(snowflake.style.animationDuration) * 1000);
	}

	stopSnowfall() {
		if (this.intervalId !== null) {
			clearInterval(this.intervalId);
			this.intervalId = null;
		}
	}

	snowflakeClickEffect(event) {
		const numSnowflakes = Math.ceil(Math.random() * 10);
		for (let i = 0; i < numSnowflakes; i++) {
			const randomX = event.clientX + Math.random() * 50 - 50;
			const randomY = event.clientY - Math.random() * 100;
			this.createSnowflake(randomX, randomY);
		}
	}
}
