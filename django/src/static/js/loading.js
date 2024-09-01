function showLoadingEffect(duration) {
	// Create the loading overlay
	const overlay = document.createElement('div');
	overlay.className = 'loading-overlay';

	// Create the spinner
	const spinner = document.createElement('div');
	spinner.className = 'spinner';
	overlay.appendChild(spinner);

	// Append the overlay to the body
	document.body.appendChild(overlay);

	if (duration) {
		// Remove the loading effect after the specified duration
		setTimeout(() => {
			document.body.removeChild(overlay);
		}, duration);
		return;
	}

	// maximum loading 10 seconds
	setTimeout(() => {
		if (document.body.contains(overlay)) {
			document.body.removeChild(overlay);
		}
	}, 10000);

	// Return a function that removes the loading effect
	return () => {
		document.body.removeChild(overlay);
	};
}

window.showLoadingEffect = showLoadingEffect;
