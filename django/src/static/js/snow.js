function createSnowflake() {
	const randomSeed = Math.random();
	const snowflake = document.createElement('div');
	snowflake.classList.add('snowflake');
	snowflake.style.left = Math.random() * 100 + 'vw';
	snowflake.style.top = '-100px';
	snowflake.style.animationDelay = '0s';
	snowflake.style.animationDuration = Math.random() * 3 + 2 + 's'; // Between 2 and 5 seconds
	snowflake.style.animationName =
		'fall, ' + (Math.random() > 0.5 ? 'spin-clockwise' : 'spin-anticlockwise');
	snowflake.style.opacity = randomSeed;
	snowflake.style.width = snowflake.style.height = randomSeed * 70 + 10 + 'px'; // Size between 10px and 20px
	snowflake.innerHTML =
		'<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/White_Snowflake.svg/2048px-White_Snowflake.svg.png" alt="Snowflake" style="width: 100%; height: 100%;">';

	document.body.appendChild(snowflake);

	// Remove snowflake after it falls
	setTimeout(() => {
		snowflake.remove();
	}, parseInt(snowflake.style.animationDuration) * 1000); // Matches longest possible animation duration
}

// Create a new snowflake every 300 milliseconds
setInterval(createSnowflake, 200);
