export class Snowfall {
	constructor() {
		this.intervalId = null;

		this.snowflakeImage = new Image();
		this.snowflakeImage.src =
			'https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/White_Snowflake.svg/2048px-White_Snowflake.svg.png';
		this.snowflakeImage.alt = 'Snowflake';

		// document.addEventListener('click', this.snowflakeClickEffect.bind(this));
	}

	startSnowfall() {
		if (this.intervalId === null) {
			this.intervalId = setInterval(this.createSnowflake.bind(this), 100);
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
