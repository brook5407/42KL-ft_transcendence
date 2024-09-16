import { router } from './spa/navigation.js';
import { getCurrentUser } from './auth.js';
import { openModal } from './spa/modal.js';
import { openDrawer } from './spa/drawer.js';

router();

getCurrentUser();

document.addEventListener('DOMContentLoaded', function(e) {
	const autoOpenItems = document.querySelectorAll('.auto-open');

	autoOpenItems.forEach((item) => {
		const type = item.value;
		const name = item.getAttribute('data-name');
		const url = item.getAttribute('data-url');
		if (type === 'modal') {
			openModal(name, { url: url });
		} else if (type === 'drawer') {
			openDrawer(name, { url: url });
		}
	});
});