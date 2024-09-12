HTMLElement.prototype.addOnlineStatus = function () {
	// if this is a img tag, add the online status dot to the parent element
	if (this.tagName === 'IMG') {
		this.parentElement.addOnlineStatus();
		return;
	}

	let dot = this.querySelector('div.online-status-dot');
	if (dot) {
		return;
	}

	dot = document.createElement('div');
	dot.style.position = 'absolute';
	dot.style.bottom = '0';
	dot.style.right = '0';
	dot.style.width = '12px';
	dot.style.height = '12px';
	dot.style.backgroundColor = '#48F059';
	dot.style.borderRadius = '50%';
	dot.classList.add('online-status-dot');

	this.style.position = 'relative'; // Ensure the parent element is positioned
	this.appendChild(dot);
};

HTMLElement.prototype.removeOnlineStatus = function () {
	// if this is a img tag, add the online status dot to the parent element
	if (this.tagName === 'IMG') {
		this.parentElement.removeOnlineStatus();
		return;
	}

	let dot = this.querySelector('div.online-status-dot');
	if (dot) {
		dot.remove();
	}
};
