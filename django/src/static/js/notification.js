// Function to play notification sound
function playNotificationSound() {
	const audio = new Audio('path/to/notification-sound.mp3'); // TODO: Replace with path to notification sound
	audio.play();
}

// Extend HTMLElement prototype
HTMLElement.prototype.notify = function (playSound = true) {
	// Play notification sound
	if (playSound) {
		playNotificationSound();
	}

	// Create notification dot
	const dot = document.createElement('div');
	dot.style.position = 'absolute';
	dot.style.top = '0';
	dot.style.right = '0';
	dot.style.width = '10px';
	dot.style.height = '10px';
	dot.style.backgroundColor = 'red';
	dot.style.borderRadius = '50%';
	dot.style.zIndex = '1000';

	dot.classList.add('notification-dot');

	// Ensure the element has position relative or absolute
	if (window.getComputedStyle(this).position === 'static') {
		this.style.position = 'relative';
	}

	// Append the dot to the element
	this.appendChild(dot);

	// Remove notification dot when clicked
	this.addEventListener('click', function () {
		this.removeNotificationDot();
	});
};

// remove notification dot when clicked
HTMLElement.prototype.removeNotificationDot = function () {
	this.querySelector('div.notification-dot').remove();
};
