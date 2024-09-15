import { GenericDrawer } from './GenericDrawer.js';

/**
 * @borrows {import("../../../types.js").ActiveChatRoom}
 * @borrows {import('../../../types.js').ChatRoom}
 * @borrows {import('../../../types.js').WSChatMessage}
 */

export class ChatListDrawer extends GenericDrawer {
	constructor(params) {
		super(params);

		/** @type {ActiveChatRoom[]} */
		this.chatRooms = [];

		this.chatListContainer = null;

		this.nextPage = 1;
		this.stillHasNextPage = true;
		this.renderingNextPage = false;
	}

	// override
	async handleDrawerOpened(e) {
		this.chatListContainer = document.querySelector('#chat-list');

		if (!this.chatListContainer) {
			return;
		}

		this.renderNextPageChatRooms();
	}

	/**
	 * @returns {Promise<ActiveChatRoom[]>}
	 */
	async fetchNextPageChatRooms() {
		const res = await ajaxWithAuth('/api/active-chat/', {
			method: 'GET',
			params: {
				page: this.nextPage,
			},
		});

		if (!res.ok) {
			return [];
		}

		const data = await res.json();
		console.log(data);
		this.nextPage++;
		if (!data.next) {
			this.stillHasNextPage = false;
		}

		/** @type {ActiveChatRoom[]} */
		const chatRooms = data.results;

		this.pushUniqueChatRooms(chatRooms);
		return chatRooms;
	}

	/**
	 *
	 * @param {ActiveChatRoom[]} chatRooms
	 */
	pushUniqueChatRooms(chatRooms) {
		chatRooms.forEach((chatRoom) => {
			const isUnique = !this.chatRooms.some(
				(existingRoom) => existingRoom.id === chatRoom.id
			);
			if (isUnique) {
				this.chatRooms.push(chatRoom);
			}
		});
	}

	/**
	 *
	 * @param {ActiveChatRoom} roomId
	 * @returns
	 */
	async fetchOneChatRoom(roomId) {
		const res = await ajaxWithAuth(
			`/api/active-chat/get-from-roomid/${roomId}/`,
			{
				method: 'GET',
			}
		);

		if (!res.ok) {
			return null;
		}

		/** @type {ActiveChatRoom} */
		const data = await res.json();
		return data;
	}

	async renderNextPageChatRooms() {
		let hadShowMoreButton = false;
		const showMoreButton = this.chatListContainer.querySelector(
			'#show-more-chat-rooms'
		);
		if (showMoreButton) {
			hadShowMoreButton = true;
			showMoreButton.remove();
		}

		const chatRooms = await this.fetchNextPageChatRooms();
		this.appendChatRooms(chatRooms);

		if (this.stillHasNextPage) {
			const showMoreButton = document.createElement('button');
			showMoreButton.id = 'show-more-chat-rooms';
			showMoreButton.textContent = 'Show more';
			showMoreButton.addEventListener('click', () => {
				this.renderNextPageChatRooms();
			});
			this.chatListContainer.appendChild(showMoreButton);
		} else if (hadShowMoreButton) {
			const noMoreRooms = document.createElement('div');
			noMoreRooms.textContent = 'No more chat rooms';
			this.chatListContainer.appendChild(noMoreRooms);
		}
	}

	/**
	 *
	 * @param {string} roomId
	 * @param {WSChatMessage} wsChatMessage
	 */
	moveChatRoomToTop(roomId, wsChatMessage = {}) {
		const chatRoomElement = this.chatListContainer.querySelector(
			`.chat-list-item[data-room-id="${roomId}"]`
		);

		if (chatRoomElement) {
			// Remove the element from its current position
			chatRoomElement.remove();

			if (Object.keys(wsChatMessage).length > 0) {
				// Update the element with the new data
				chatRoomElement.querySelector('.last-message-sender').textContent =
					wsChatMessage.sender.nickname;
				chatRoomElement.querySelector('.last-message').textContent =
					wsChatMessage.message;
				chatRoomElement
					.querySelector('.chat-time')
					.setAttribute('data-timestamp', Date.now());
				chatRoomElement.querySelector('div.chat-image').addUnreadCount(1);
			}
			// Add the element to the top of the list
			this.chatListContainer.prepend(chatRoomElement);

			// Apply the animation class
			chatRoomElement.classList.add('animate');

			// Remove the animation class after the animation ends
			chatRoomElement.addEventListener('animationend', () => {
				chatRoomElement.classList.remove('animate');
			});
		} else {
			this.fetchOneChatRoom(roomId)
				.then((chatRoom) => {
					this.addChatRoomToTop(chatRoom);
				})
				.catch((err) => {
					console.error(err);
				});
		}
	}

	/**
	 *
	 * @param {ActiveChatRoom} chatRoom
	 */
	addChatRoomToTop(chatRoom) {
		const chatRoomElement = this.createChatRoomElement(chatRoom);

		// Add the new chat room element to the top of the list
		this.chatListContainer.prepend(chatRoomElement);

		// Apply the animation class
		chatRoomElement.classList.add('animate');

		// Remove the animation class after the animation ends
		chatRoomElement.addEventListener('animationend', () => {
			chatRoomElement.classList.remove('animate');
		});
	}

	/**
	 *
	 * @param {ActiveChatRoom[]} chatRooms
	 */
	appendChatRooms(chatRooms) {
		chatRooms.forEach((chatRoom) => {
			console.log(chatRoom);
			const chatRoomElement = this.createChatRoomElement(chatRoom);
			this.chatListContainer?.appendChild(chatRoomElement);
		});
	}

	/**
	 *
	 * @param {ActiveChatRoom} chatRoom
	 * @returns {HTMLDivElement}
	 */
	createChatRoomElement(chatRoom) {
		const div = document.createElement('div');
		div.className = 'chat-list-item';
		div.dataset.roomId = chatRoom.room.id;
		div.innerHTML = `
            <div class="chat-image">
                <img src="${chatRoom.room.cover_image}"
                    alt="${chatRoom.room.name} cover image"
                    width="50"
                    height="50"
                />
            </div>
            <div class="chat-details">
                <div class="chat-name">${chatRoom.room.name}</div>
                    <div class="last-message-container">
                        <div class="last-message-sender">${
													chatRoom.last_message?.sender.nickname || ''
												}</div>
                        <div class="last-message">${
													chatRoom.last_message?.message || ''
												}</div>
                    </div>
            </div>
            <div class="chat-time" data-timestamp="${
							chatRoom.last_message?.created_at
						}"></div>
        `;

		// Add unread count
		div.querySelector('div.chat-image').addUnreadCount(chatRoom.unread_count);

		// Add a colon after the sender's name if it exists
		if (div.querySelector('.last-message-sender').textContent) {
			div.querySelector('.last-message-sender').textContent += ': ';
		}

		// click to chat room
		div.addEventListener('click', () => {
			openDrawer('chat-room', {
				url: 'drawer/chat-room',
				queryParams: {
					room_id: chatRoom.room.id,
				},
			});
		});

		// format the last message timestamp if exist
		if (chatRoom.last_message) {
			this.formatLastMessageTime(div);
		}

		return div;
	}

	formatLastMessageTime(div) {
		const timeElement = div.querySelector('.chat-time');
		if (!timeElement) {
			return;
		}
		const timestamp = timeElement.getAttribute('data-timestamp');
		if (!timestamp) {
			return;
		}
		const date = new Date(timestamp);
		const formattedTime = dateFns.formatDistanceToNow(date, {
			addSuffix: true,
		});
		timeElement.textContent = formattedTime;
	}
}
