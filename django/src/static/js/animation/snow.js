export class Snowfall {
	constructor() {
		this.snowflakeCount = 50; // WXR TODO: make this adjustable in settings drawer
		this.snowflakes = [];
		this.snowflakeImageSrc = '/static/images/snowflake.svg';
	}

	async createSnowflakes() {
		const createOneSnowflake = () => {
			const snowflake = new Image();
			snowflake.src = this.snowflakeImageSrc;
			snowflake.alt = 'Snowflake';
			snowflake.classList.add('blur');
			snowflake.classList.add('snowflake');
			snowflake.style.left = Math.random() * 100 + 'vw';
			snowflake.style.animationDelay = '0s';
			snowflake.style.animationDuration = Math.random() * 3 + 2 + 's';
			snowflake.style.animationTimingFunction = 'linear';
			snowflake.style.width = snowflake.style.height =
				Math.random() * 30 + 10 + 'px';
			snowflake.style.opacity = Math.random();

			// Randomly assign spin animation

			// snowflake.style.animationIterationCount = 'infinite';
			// snowflake.style.zIndex = Math.min(Math.floor(Math.random() * 100), 1000);
			snowflake.style.zIndex = -1;

			// void snowflake.offsetWidth;

			document.body.appendChild(snowflake);
			this.snowflakes.push(snowflake);

			const spinAnimation =
				Math.random() > 0.5 ? 'spin-clockwise' : 'spin-anticlockwise';
			snowflake.style.animationName = `fall, ${spinAnimation}`;

			// Add event listener to reset snowflake position when animation ends
			snowflake.addEventListener('animationend', () => {
				this.resetSnowflake(snowflake);
			});
		};

		// create snowflakes with a little delay between each
		for (let i = 0; i < this.snowflakeCount; i++) {
			// sleep is a helper functino in utils.js
			await sleep(Math.random() * 100);
			createOneSnowflake();
		}
	}

	resetSnowflake(snowflake) {
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
		this.createSnowflakes();
	}

	stopSnowfall() {
		this.snowflakes.forEach((snowflake) => {
			snowflake.remove();
		});
		this.snowflakes = [];
	}
}
