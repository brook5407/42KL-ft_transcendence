export class Snowfall {
	constructor() {
		this.snowflakeCount = 50; // WXR TODO: make this adjustable in settings drawer
		this.snowflakes = [];
		this.snowflakeImageSrc = '/static/images/snowflake.svg';

		this.createSnowflakes();
	}

	createSnowflakes() {
		for (let i = 0; i < this.snowflakeCount; i++) {
			const snowflake = new Image();
			snowflake.src = this.snowflakeImageSrc;
			snowflake.alt = 'Snowflake';
			snowflake.classList.add('snowflake');
			snowflake.style.position = 'absolute';
			snowflake.style.top = '-50px'; // Start above the viewport
			snowflake.style.left = Math.random() * 100 + 'vw';
			snowflake.style.width = snowflake.style.height =
				Math.random() * 30 + 10 + 'px';
			snowflake.style.opacity = Math.random();
			snowflake.style.animationDuration = Math.random() * 3 + 2 + 's'; // Between 2 and 5 seconds

			// Randomly assign spin animation
			const spinAnimation =
				Math.random() > 0.5 ? 'spinClockwise' : 'spinAnticlockwise';
			snowflake.style.animationName = `fall, ${spinAnimation}`;
			snowflake.style.animationTimingFunction = 'linear';
			snowflake.style.animationIterationCount = 'infinite';
			snowflake.style.zIndex = -1;

			void snowflake.offsetWidth;

			document.body.appendChild(snowflake);
			this.snowflakes.push(snowflake);

			// Add event listener to reset snowflake position when animation ends
			snowflake.addEventListener('animationend', () => {
				this.resetSnowflake(snowflake);
			});
		}
	}

	resetSnowflake(snowflake) {
		snowflake.style.top = '-50px'; // Reset to above the viewport
		snowflake.style.left = Math.random() * 100 + 'vw';
		snowflake.style.animationDuration = Math.random() * 3 + 2 + 's'; // Between 2 and 5 seconds
		snowflake.style.animationName = 'none'; // Reset animation
		// Trigger reflow to restart animation
		void snowflake.offsetWidth;
		const spinAnimation =
			Math.random() > 0.5 ? 'spin-clockwise' : 'spin-anticlockwise';
		snowflake.style.animationName = `fall, ${spinAnimation}`;
	}

	startSnowfall() {
		this.snowflakes.forEach((snowflake) => {
			snowflake.style.animationName = `fall, ${
				Math.random() > 0.5 ? 'spin-clockwise' : 'spin-anticlockwise'
			}`;
		});
	}

	stopSnowfall() {
		this.snowflakes.forEach((snowflake) => {
			snowflake.style.animationName = 'none';
		});
	}
}
