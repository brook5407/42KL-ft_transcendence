import { showSuccessMessage, showInfoMessage } from './message.js';
import { closeModal } from './spa/modal.js';
import { router } from './spa/navigation.js';
import { ajax } from './spa/ajax.js';

export function signup(data) {
	closeModal();
	showSuccessMessage('Please check your email to verify your account!');
	router();
}

export function signin(data) {
	localStorage.setItem('access_token', data.access);
	localStorage.setItem('refresh_token', data.refresh);

	closeModal();
	showSuccessMessage('You have successfully signed in!');
	router();
}

export function logout() {
	localStorage.removeItem('access_token');
	localStorage.removeItem('refresh_token');
	showInfoMessage('You have successfully logged out!');
	router();
}

document.addEventListener('DOMContentLoaded', function () {
	document.body.addEventListener('click', function (event) {
		if (event.target.matches('#logout-button')) {
			ajax('/auth/signout', {
				method: 'POST',
			})
			.then((response) => {
				if (response.ok) {
					logout();
				}
			});
		}
	});
});

document.addEventListener('DOMContentLoaded', function() {
    const otpButton = document.getElementById('send-otp-button');

    otpButton.addEventListener('click', function() {
        fetch('{% url "send_otp" %}', {  // Replace with your actual URL name
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
            } else {
                alert('Error requesting OTP. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error requesting OTP. Please try again.');
        });
    });
});