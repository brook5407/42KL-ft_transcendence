import { ajaxWithAuth } from '../../ajax.js';
import { GenericDrawer } from './GenericDrawer.js';

/**
 * @borrows {import('../../../types.js').WSChatMessage}
 * @borrows {import('../../../types.js').Profile}
 */

const MAX_MESSAGE_LENGTH = 50;

export class ChatRoomDrawer extends GenericDrawer {
	constructor(params) {
		super(params);

		this.room_id = null;
		this.isGroupChat = false;
		this.lastInviteTimestamp = null;

		this.spinnerHTML = `
			<div class="spinner-border text-primary" role="status">
				<span class="sr-only">Loading...</span>
			</div>
		`;
		this.spinnerElement = null;
		this.chatMessagesContainer = null;

		/** @type {WSChatMessage[]} */
		this.chatMessages = [];

		this.nextPage = 1;
		this.stillHasNextPage = true;
		this.renderingNextPage = false;
	}

	async fetchNextPageHistoryMessages() {
		const res = await ajaxWithAuth(
			`/api/chat-message/${this.room_id}/history/`,
			{
				method: 'GET',
				params: {
					page: this.nextPage,
				},
			}
		);

		if (!res.ok) {
			return [];
		}

		const data = await res.json();
		this.nextPage++;
		if (!data.next) {
			this.stillHasNextPage = false;
		}
		const messages = data.results;
		this.chatMessages.push(messages);
		return messages;
	}

	async renderNextPageMessages() {
		this.renderingNextPage = true;

		/** @type {Message[]} */
		const messages = await this.fetchNextPageHistoryMessages();
		this.hideLoadingSpinner();

		messages.forEach((message) => {
			this.prependMessage(message);
		});

		this.renderingNextPage = false;
	}

	showLoadingSpinner() {
		this.spinnerElement = document.createElement('div');
		this.spinnerElement.id = 'loading-spinner';
		this.spinnerElement.innerHTML = this.spinnerHTML;
		this.chatMessagesContainer.prepend(this.spinnerElement);
	}

	hideLoadingSpinner() {
		if (!this.spinnerElement) {
			return;
		}
		this.spinnerElement.remove();
		this.spinnerElement = null;
	}

	// override
	async handleDrawerOpened(e) {
		if (e.detail.drawerName !== 'chat-room') {
			return;
		}

		this.room_id = this.queryParams.room_id;
		if (!this.room_id) {
			this.room_id = JSON.parse(
				document.querySelector('#room_id')?.textContent || '""'
			);
		}
		this.isGroupChat = this.props.is_group_chat;

		// mark the chat as read
		ajaxWithAuth(`/api/active-chat/mark-read/${this.room_id}/`, {
			method: 'POST',
		});

		// focus on the chat input when the drawer is opened
		const chatInput = this.element.querySelector('#message-input');
		chatInput.focus();

		this.chatMessagesContainer = this.element.querySelector('#chat-messages');
		this.showLoadingSpinner();
		await this.renderNextPageMessages();
		this.scrollToBottom();
		this.chatMessagesContainer.addEventListener('wheel', () => {
			if (
				!this.renderingNextPage &&
				this.chatMessagesContainer.scrollTop <= 0
			) {
				this.showLoadingSpinner();
				if (!this.stillHasNextPage) {
					this.hideLoadingSpinner();
					return;
				}
				this.renderNextPageMessages();
			}
		});

		const sendMessage = (value) => {
			let message = value;
			if (!message) {
				const chatInput = this.element.querySelector('#message-input');
				message = chatInput.value;
      }
			if (message.length > MAX_MESSAGE_LENGTH) {
				alert(`Message is too long! Please limit your message to ${MAX_MESSAGE_LENGTH} characters.`);
				return;
			}
			if (!message) {
				return;
			}
			chatInput.value = '';
			window.chatController.sendMessage(message, this.room_id);
		};

		chatInput.addEventListener('keydown', (e) => {
			if (e.key === 'Enter') {
				e.preventDefault();
				sendMessage();
			}
		});

		const inviteButton = this.element.querySelector('#pong-invite-icon');
		if (inviteButton) {
			inviteButton.addEventListener('click', () => {
				if (
					this.lastInviteTimestamp &&
					Date.now() - this.lastInviteTimestamp < 5000
				) {
					return;
				}
				// if accepted
				// 		if the sender user online redirect both user to the pong page
				//		if the sender user offline, show a toast message showing the sender user is offline
				// if rejected, show a toast message to sender if online, showing the invite is rejected
				// friend games are not gonna affect ELO points
				sendMessage('/invite');
				this.lastInviteTimestamp = Date.now();
				inviteButton.classList.add('disabled');
				setTimeout(() => {
					inviteButton.classList.remove('disabled');
				}, 5000);
			});
		}

		const sendButton = this.element.querySelector('#send-button');
		sendButton.addEventListener('click', sendMessage);
	}

	wrapUrlsWithAnchorTags(message) {
		const urlPattern =
			/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gi;
		return message.replace(urlPattern, '<a href="$1" target="_blank">$1</a>');
	}

	/**
	 * Format the timestamp based on the difference between the current date and the message date.
	 * @param {Date} timestamp - The timestamp of the message.
	 * @returns {string} - The formatted timestamp.
	 */
	formatTimestamp(timestamp) {
		const now = new Date();
		const messageDate = new Date(timestamp);
		const diffDays = now.getDate() - messageDate.getDate();

		if (diffDays === 0) {
			return `Today, ${messageDate.toLocaleTimeString('en-US', {
				hour: '2-digit',
				minute: '2-digit',
			})}`;
		} else if (diffDays === 1) {
			return `Yesterday, ${messageDate.toLocaleTimeString('en-US', {
				hour: '2-digit',
				minute: '2-digit',
			})}`;
		} else if (diffDays < 7) {
			return `${diffDays} days ago, ${messageDate.toLocaleTimeString('en-US', {
				hour: '2-digit',
				minute: '2-digit',
			})}`;
		} else {
			return messageDate.toLocaleString('en-US', {
				weekday: 'short', // e.g., 'Mon'
				month: 'short', // e.g., 'Oct'
				day: '2-digit', // e.g., '01'
				year: 'numeric', // e.g., '2023'
				hour: '2-digit', // e.g., '01 PM'
				minute: '2-digit', // e.g., '30'
			});
		}
	}

	/**
	 *
	 * @param {WSChatMessage|Message} message
	 * @returns {string}
	 */
	renderMessageBubble(message) {
		let invitationExpiresAt = null;
		if (message.match_invitation && message.match_invitation.expired_at) {
			invitationExpiresAt = new Date(message.match_invitation.expired_at);
		} else if (
			!message.match_invitation &&
			message.message.startsWith('/invite')
		) {
			invitationExpiresAt = new Date();
			invitationExpiresAt.setMinutes(invitationExpiresAt.getMinutes() + 5);
		}
		if (message.match_invitation || message.message.startsWith('/invite')) {
			const status = message.match_invitation?.status || 'W';
			return `
				<div class="chat-room__message-card" data-status="${status}" data-expires-at="${invitationExpiresAt?.toISOString()}">
					<div class="chat-room__message-card-title">Jom Pong!</div>
					<div class="chat-room__message-card-icon">🏓</div>
					<div class="chat-room__message-card-status"></div>
					<div class="chat-room__message-card-buttons">
						<button class="chat-room__message-card-button chat-room__pong-accept-button">Accept</button>
						<button class="chat-room__message-card-button chat-room__pong-reject-button">Reject</button>
					</div>
				</div>
			`;
		} else {
			return `
				<div class="chat-room__message-bubble">${this.wrapUrlsWithAnchorTags(
					message.message
				)}</div>
			`;
		}
	}

	/**
	 *
	 * @param {WSChatMessage|Message} message
	 * @returns {HTMLDivElement}
	 */
	createMessageElement(message, isInviteMessage = false) {
		const isSentByCurrentUser =
			message.sender.username === currentUser.username;
		const messageClass = isSentByCurrentUser
			? 'chat-room__message-sent'
			: 'chat-room__message-received';
		const timestamp = new Date(message.created_at);
		const formattedTimestamp = this.formatTimestamp(timestamp);

		const messageElem = document.createElement('div');
		messageElem.className = `chat-room__message ${messageClass}`;
		messageElem.innerHTML = `
			<div class="chat-room__avatar-container">
				<span class="chat-room__nickname">${message.sender.profile.nickname}</span>
				<img src="${message.sender.profile.avatar}" alt="${
			message.sender.profile.nickname
		}'s avatar" class="chat-room__avatar">
			</div>
			${this.renderMessageBubble(message)}
			<div class="chat-room__timestamp">${formattedTimestamp}</div>
		`;

		const avatar = messageElem.querySelector('img.chat-room__avatar');
		if (!isSentByCurrentUser) {
			avatar.addEventListener('click', () => {
				openDrawer('friend-profile', {
					url: `drawer/friend-drawer`,
					queryParams: {
						username: message.sender.username,
					},
				});
			});
		} else {
			avatar.addEventListener('click', () => {
				openDrawer('profile', {
					url: `drawer/profile/`,
				});
			});
		}

		if (message.match_invitation || message.message.startsWith('/invite')) {
			const invitationCard = messageElem.querySelector(
				'.chat-room__message-card'
			);
			const invitationStatusContainer = invitationCard.querySelector(
				'.chat-room__message-card-status'
			);
			const acceptButton = invitationCard.querySelector(
				'.chat-room__pong-accept-button'
			);
			const rejectButton = invitationCard.querySelector(
				'.chat-room__pong-reject-button'
			);
			const invitationStatus = invitationCard.getAttribute('data-status');
			if (invitationStatus === 'W') {
				const expiredAtString = invitationCard.getAttribute('data-expires-at');
				const expiresAt = new Date(expiredAtString);
				const currentTime = Date.now();
				let remainingTime = Math.floor((expiresAt - currentTime) / 1000);

				if (remainingTime <= 0) {
					// If the invitation is already expired
					invitationStatusContainer.textContent = 'Expired';
					acceptButton.disabled = true;
					rejectButton.disabled = true;
					acceptButton.classList.add('disabled');
					rejectButton.classList.add('disabled');
				} else {
					// Initialize the countdown timer
					invitationStatusContainer.textContent = `Expires in ${remainingTime} seconds`;

					const countdownInterval = setInterval(() => {
						remainingTime -= 1;
						invitationStatusContainer.textContent = `Expires in ${remainingTime} seconds`;

						if (remainingTime <= 0) {
							clearInterval(countdownInterval);
							invitationStatusContainer.textContent = 'Expired';
							acceptButton.disabled = true;
							rejectButton.disabled = true;
							acceptButton.classList.add('disabled');
							rejectButton.classList.add('disabled');
						}
					}, 1000);

					if (!isSentByCurrentUser) {
						acceptButton.addEventListener('click', () => {
							// if the sender user is online, redirect both user to the pong page
							// if the sender user is offline, show a toast message showing the sender user is offline
							window.chatController.acceptPongInvitation(
								this.room_id,
								message.match_invitation?.id || message.match_invitation_id
							);
						});

						rejectButton.addEventListener('click', () => {
							window.chatController.rejectPongInvitation(
								this.room_id,
								message.match_invitation?.id || message.match_invitation_id
							);
						});
					} else {
						acceptButton.disabled = true;
						rejectButton.disabled = true;
						acceptButton.classList.add('disabled');
						rejectButton.classList.add('disabled');
					}
				}
			} else {
				invitationStatusContainer.textContent =
					invitationStatus === 'A' ? 'Accepted' : 'Rejected';
				acceptButton.disabled = true;
				rejectButton.disabled = true;
				acceptButton.classList.add('disabled');
				rejectButton.classList.add('disabled');
			}
		}

		return messageElem;
	}

	/**
	 *
	 * @param {WSChatMessage} message
	 * @returns
	 */
	prependMessage(message) {
		if (!this.chatMessagesContainer) {
			return;
		}
		const messageElem = this.createMessageElement(message);
		this.chatMessagesContainer.prepend(messageElem);
	}

	/**
	 *
	 * @param {WSChatMessage} message
	 * @returns
	 */
	appendMessage(message) {
		if (!this.chatMessagesContainer) {
			return;
		}
		const messageElem = this.createMessageElement(message);
		this.chatMessagesContainer.appendChild(messageElem);
		this.scrollToBottom();
	}

	scrollToBottom() {
		// scroll to bottom
		this.chatMessagesContainer.scrollTo({
			top: this.chatMessagesContainer.scrollHeight,
			behavior: 'smooth',
		});
	}
}
