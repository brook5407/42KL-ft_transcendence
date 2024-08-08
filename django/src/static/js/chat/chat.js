const host = window.location.hostname;
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const port = window.location.port || (protocol === 'wss:' ? '443' : '80');

const appConfigElement = document.getElementById('chat-config');
const nickname = appConfigElement.getAttribute('data-nickname'); //
const group_num = appConfigElement.getAttribute('data-room') || 123;
console.log('nickname: ' + nickname);

// const ChatListConfigElement = document.getElementById('chat-list-item');
// const group_num = ChatListConfigElement.getAttribute('data-roomid') || 123;

// let currentUrl = window.location.href;
// let url = new URL(currentUrl);
// let group_num = url.searchParams.get('room') || 123;

//Testing purpose
async function fetchToken() {
	const queryString = new URLSearchParams({
		group_num: group_num ? group_num : '123',
		nickname: 'JohnDoe',
		// nickname: nickname ? nickname : 'JohnDoe'
	}).toString();

	const response = await fetch('/chat?' + queryString);
	// console.log('/chat?' + queryString);
	const chat_data = await response.json();
	return chat_data.token;
}

async function initialize() {
	try {
		// Fetch the token
		const token = await fetchToken();

		// Use the token
		console.log('Retrieved token:', token);

		// Further actions with the token, e.g., decode or use in application
		// Note: Ensure any sensitive operations are done securely
	} catch (error) {
		console.error('Error initializing:', error);
	}
}
initialize();

//Testing purpose
async function fetchToken() {
	const queryString = new URLSearchParams({
		group_num: group_num ? group_num : '123',
		nickname: 'JohnDoe',
		// nickname: nickname ? nickname : 'JohnDoe'
	}).toString();

	const response = await fetch('/chat?' + queryString);
	// console.log('/chat?' + queryString);
	const chat_data = await response.json();
	return chat_data.token;
}

async function initialize() {
	try {
		// Fetch the token
		const token = await fetchToken();

		// Use the token
		console.log('Retrieved token:', token);

		// Further actions with the token, e.g., decode or use in application
		// Note: Ensure any sensitive operations are done securely
	} catch (error) {
		console.error('Error initializing:', error);
	}
}
initialize();

async function fetchToken() {
	const queryString = new URLSearchParams({
		group_num: group_num ? group_num : '123',
		nickname: 'JohnDoe',
		// nickname: nickname ? nickname : 'JohnDoe'
	}).toString();

	const response = await fetch('/chat?' + queryString);
	// console.log('/chat?' + queryString);
	const chat_data = await response.json();
	return chat_data.token;
}

async function initialize() {
	try {
		// Fetch the token
		const token = await fetchToken();

		// Use the token
		console.log('Retrieved token:', token);

		// Further actions with the token, e.g., decode or use in application
		// Note: Ensure any sensitive operations are done securely
	} catch (error) {
		console.error('Error initializing:', error);
	}
}
initialize();

const socketURL = `${protocol}//${host}:${port}/room/${group_num}/?customer_name=${nickname}`;
let socket = null;

function newSocket() {
	if (socket !== null && socket.readyState === WebSocket.OPEN) {
		socket.close();
	}

	socket = new WebSocket(socketURL);

	socket.onopen = function (event) {
		handleSocketOpen();
	};

	socket.onmessage = function (event) {
		handleSocketMessage(event);
	};

	socket.onclose = function (event) {
		handleSocketClose();
	};

	socket.onerror = function (error) {
		console.error('WebSocket error:', error);
	};
}

function openConnect() {
	if (socket.readyState === WebSocket.OPEN) return;
	newSocket();
}

newSocket();

function closeConnect() {
	if (socket) {
		socket.close(); // Close the connection
	}
}

function handleSocketOpen() {
	console.log('WebSocket connection opened.');
	appendStatusMessage('连接成功', 'green', '你有朋友了 (｡♥‿♥｡)\n');
}

function handleSocketMessage(event) {
	const data = JSON.parse(event.data);
	if (data.type === 'message') {
		displayChatMessage(data.message, data.name);
	} else if (data.type === 'image') {
		displayImage(data.image, data.name);
	} else {
		displayChatMessage(data.message, data.name);
	}
	scrollToBottom();
}

function handleSocketClose() {
	console.log('WebSocket connection closed.');
	logMessage(nickname + '连接已断开', 'error');
	appendStatusMessage('连接关闭', 'red', '你没朋友了 ｡ﾟ･ (>﹏<) ･ﾟ｡\n');
}

document.getElementById('fileInput').addEventListener('change', handleUpload);
function handleUpload() {
	const fileInput = document.getElementById('fileInput');
	const file = fileInput.files[0];

	if (file) {
		const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB

		if (file.size > MAX_FILE_SIZE) {
			alert('File size exceeds the 5 MB limit.');
			return; // Exit the function if file size is too large
		}
		const reader = new FileReader();

		reader.onload = function (event) {
			const imageUrl = event.target.result;

			// Display the uploaded image immediately
			// displayImage(imageUrl);

			// Send the image URL via WebSocket
			socket.send(
				JSON.stringify({
					type: 'image',
					name: nickname,
					image: imageUrl,
				})
			);
		};

		reader.readAsDataURL(file);
	} else {
		alert('Please select a file to upload.');
	}
}

function displayImage(imageUrl, name) {
	const imageContainer = document.getElementById('message-container');

	// Create a container for the image and username
	const messageWrapper = document.createElement('div');
	// messageWrapper.style.display = 'inline-flex'; // Align items horizontally
	messageWrapper.style.display = 'flex'; // Align items horizontally
	messageWrapper.style.padding = '0px 0px 5px 0px';
	// messageWrapper.style.box-sizing = 'border-box';

	// Create and style the username element
	const username = document.createElement('span');
	username.textContent = name;
	username.textContent.endsWith(': ')
		? username.textContent
		: (username.textContent += '：');
	username.style.color = 'blue';
	username.style.fontWeight = 'bold';
	// username.style.width = "auto";
	username.style.display = 'inline-flex';
	username.style.marginRight = '10px';

	// Create the image element
	const imgElement = document.createElement('img');
	imgElement.src = imageUrl;
	imgElement.style.maxWidth = '100px'; // Adjust styling as needed
	imgElement.style.height = 'auto'; // Maintain aspect ratio
	imgElement.style.display = 'inline-block';

	// Add a placeholder for the image
	const placeholderUrl = 'static/images/meme/miku_impatient.png'; // Path to placeholder image
	const placeholder = document.createElement('img');
	placeholder.src = placeholderUrl;
	placeholder.style.maxWidth = '100px';
	placeholder.style.height = 'auto';
	placeholder.style.display = 'none'; // Initially hidden

	// Append username and image to the wrapper
	messageWrapper.appendChild(username);
	messageWrapper.appendChild(imgElement);
	messageWrapper.appendChild(placeholder);
	imageContainer.appendChild(messageWrapper);

	// Handle image load success
	imgElement.onload = function () {
		placeholder.style.display = 'none'; // Hide placeholder if image loads successfully
		// imageContainer.appendChild(document.createElement("div")).innerText = "\n";
		scrollToBottom();
	};

	// Handle image load error
	imgElement.onerror = function () {
		imgElement.style.display = 'none'; // Hide the actual image
		placeholder.style.display = 'inline-block'; // Show placeholder
		const errorMessage = document.createElement('div');
		errorMessage.innerText = 'Failed to load image';
		errorMessage.style.color = 'red';
		imageContainer.appendChild(errorMessage);
		scrollToBottom();
	};
}

function sendMessage() {
	if (socket.readyState === WebSocket.OPEN) {
		let message = document.getElementById('message-input').value.trim();
		// message.focus();
		// message.setSelectionRange(7, 7);
		if (message !== '') {
			socket.send(
				JSON.stringify({
					type: 'message',
					name: nickname,
					message: message,
				})
			);
			document.getElementById('message-input').value = '';
		}
	} else {
		socket_state(socket);
		openConnect();
	}
}

// url='https://upload.wikimedia.org/wikipedia/commons/0/09/Blackpink_Coachella_2023_02_%28cropped%29.jpg';

function displayChatMessage(data, name) {
	if (typeof data !== 'string') {
		console.error('Invalid input: expected a string.');
		return;
	}

	let message = document.createElement('div');
	message.style.display = 'flex';
	message.style.padding = '0px 0px 5px 0px';
	message.style.lineHeight = '0.8';

	if (data) {
		let username = document.createElement('span');
		username.textContent = name;
		username.textContent = name + ' :';
		username.style.color = 'blue';
		username.style.fontWeight = 'bold';
		username.style.width = '70px';
		username.style.marginRight = '10px';

		let placeholderContainer = document.createElement('span');
		placeholderContainer.classList.add('chatPlaceholder');

		let content = data;
		placeholderContainer.innerHTML = content;
		message.appendChild(username);
		message.appendChild(placeholderContainer);
	} else {
		let textNode = document.createElement('span');
		textNode.innerHTML = messageText;

		message.appendChild(textNode);
		message.appendChild(placeholderContainer);
	}

	let messageContainer = document.querySelector('.chat-messages');
	if (messageContainer) {
		messageContainer.appendChild(message);
	} else {
		console.error('Element with class "message" not found.');
	}
}

function appendStatusMessage(status, color, message) {
	let tag = document.createElement('div');
	tag.innerText = status;
	tag.style.color = color;
	tag.append(`\t${message}`);
	let message_sect = document.querySelector('.chat-messages');
	if (message_sect) {
		message_sect.appendChild(tag);
	}
}

function scrollToBottom() {
	var messageContainer = document.getElementById('message-container');
	messageContainer.scrollTop = messageContainer.scrollHeight;
}

function logMessage(message, style = 'default') {
	const styles = {
		default: 'color: black;',
		warning: 'color: orange; font-weight: bold;',
		error: 'color: red; font-weight: bold;',
	};
	console.log(`%c${message}`, styles[style]);
}

function socket_state(socket) {
	if (socket.readyState === WebSocket.OPEN) {
		logMessage('The connection is open', 'warning');
	} else if (socket.readyState === WebSocket.CONNECTING) {
		logMessage('The connection is connecting', 'warning');
	} else if (socket.readyState === WebSocket.CLOSING) {
		logMessage('The connection is closing', 'warning');
	} else if (socket.readyState === WebSocket.CLOSED) {
		logMessage('The connection is closed', 'warning');
	} else {
		logMessage('The connection state is unknown', 'warning');
	}
}

function handleMessage(event) {
	if (event.key === 'Enter') {
		sendMessage();
	}
}

function dataURLToBlob(dataURL) {
	const BASE64_MARKER = ';base64,';
	if (dataURL.indexOf(BASE64_MARKER) === -1) {
		const parts = dataURL.split(',');
		const contentType = parts[0].split(':')[1];
		const raw = parts[1];
		return new Blob([raw], { type: contentType });
	}

	const parts = dataURL.split(BASE64_MARKER);
	const contentType = parts[0].split(':')[1];
	const raw = window.atob(parts[1]);
	const rawLength = raw.length;

	const uInt8Array = new Uint8Array(rawLength);
	for (let i = 0; i < rawLength; ++i) {
		uInt8Array[i] = raw.charCodeAt(i);
	}

	return new Blob([uInt8Array], { type: contentType });
}
