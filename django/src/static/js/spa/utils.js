export function checkNearestMatch(element, selector, levels) {
	let currentElement = element;
	for (let i = 0; i < levels; i++) {
		if (currentElement && currentElement.matches(selector)) {
			return currentElement;
		}
		currentElement = currentElement.parentElement;
	}
	return false;
}
