window.notificationSound = new Audio('/static/audio/pop.wav');

// Function to play notification sound
window.playNotificationSound = function () {
	window.notificationSound.play();
};

HTMLElement.prototype.addUnreadCount = function (count = 1) {
	if (count <= 0) {
		return;
	}

	if (this.tagName === 'IMG') {
		this.parentElement.addUnreadCount(count);
		return;
	}

	// If the element already has a unread count, increment it
	let unreadCount = this.querySelector('div.unread-count');
	if (unreadCount) {
		unreadCount.textContent = parseInt(unreadCount.textContent) + count;
		return;
	}

	unreadCount = document.createElement('div');
	unreadCount.textContent = count;
	unreadCount.style.position = 'absolute';
	unreadCount.style.top = '-12px';
	unreadCount.style.right = '-12px';
	unreadCount.style.backgroundColor = '#FF0000';
	unreadCount.style.color = '#FFFFFF';
	unreadCount.style.borderRadius = '50%';
	unreadCount.style.padding = '2px';
	unreadCount.style.fontSize = '12px';
	unreadCount.classList.add('unread-count');

	this.appendChild(unreadCount);
};

HTMLElement.prototype.removeUnreadCount = function () {
	if (this.tagName === 'IMG') {
		this.parentElement.removeUnreadCount();
		return;
	}

	let unreadCount = this.querySelector('div.unread-count');
	if (unreadCount) {
		unreadCount.remove();
	}
};
