import { ajaxWithAuth } from '../../ajax.js';
import { Component } from '../Component.js';

export class ChatRoomDrawer extends Component {
	constructor(params) {
		super(params);

		this.boundHandleChatRoomDrawerOpened =
			this.handleChatRoomDrawerOpened.bind(this);

		this.spinner = null;
		this.chatMessagesContainer = null;

		this.nextPage = 1;
		this.stillHasNextPage = true;
		this.renderingHistoryMessage = false;
	}

	async fetchNextPageHistoryMessages() {
		const res = await ajaxWithAuth(
			`/api/chat/${this.queryParams.room_id}/history/`,
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
		return data.results;
	}

	async renderNextPageMessages() {
		this.renderingHistoryMessage = true;

		const messages = await this.fetchNextPageHistoryMessages();
		console.log(messages);

		messages.forEach((message) => {});
		const msgs = messages.map((message) => {
			const div = document.createElement('div');
			div.textContent = message.message;
			return div;
		});
		console.log(msgs);
		this.prependElements(this.chatMessagesContainer, msgs);

		this.renderingHistoryMessage = false;
		this.hideLoadingSpinner();
	}

	showLoadingSpinner() {
		if (!this.spinner) {
			return;
		}
		this.spinner.style.display = 'block';
	}

	hideLoadingSpinner() {
		if (!this.spinner) {
			return;
		}
		this.spinner.style.display = 'none';
	}

	handleChatRoomDrawerOpened(e) {
		if (e.detail.drawerName === 'chat-room') {
			this.spinner = this.element.querySelector('#loading-spinner');
			this.showLoadingSpinner();
			this.renderNextPageMessages();

			this.chatMessagesContainer = this.element.querySelector('#chat-messages');

			this.chatMessagesContainer.addEventListener('wheel', () => {
				if (
					this.stillHasNextPage &&
					!this.renderingHistoryMessage &&
					this.chatMessagesContainer.scrollTop <= 0
				) {
					this.showLoadingSpinner();
					this.renderNextPageMessages();
				}
			});
		}
	}

	prependElements(container, elements) {
		elements.forEach((element) => {
			container.insertBefore(element, container.firstChild);
		});
	}

	// override
	startComponent() {}

	// override
	async initComponent() {
		document.addEventListener(
			'drawer-opened',
			this.boundHandleChatRoomDrawerOpened
		);
	}

	// override
	destroy() {
		super.destroy();
		document.removeEventListener(
			'drawer-opened',
			this.boundHandleChatRoomDrawerOpened
		);
	}

	template() {
		return `
			<div>
				<h1>Drawer</h1>
			</div>
		`;
	}
}
