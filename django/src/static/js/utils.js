window.getCookie = function (name) {
	const nameEQ = name + '=';
	const ca = document.cookie.split(';');
	for (let i = 0; i < ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) === ' ') c = c.substring(1, c.length);
		if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
	}
	return null;
};

window.deleteCookie = function (name) {
	document.cookie = name + '=; Max-Age=-99999999;';
};

window.isHTMLElement = function (str) {
	const tempDiv = document.createElement('div');
	tempDiv.innerHTML = str.trim();
	return tempDiv.childNodes.length > 0 && tempDiv.childNodes[0].nodeType === 1;
};
