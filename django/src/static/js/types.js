/**
 * @typedef {Object} WSChatMessage
 * @property {WSChatMessageErrorType} [error] - The error type (optional).
 * @property {string} [type] - The message type, group or private (optional).
 * @property {string} message - The message content.
 * @property {Profile} sender - The sender profile of the message.
 * @property {string} room_id - The ID of the room.
 * @property {string} room_name - The name of the room.
 * @property {string} [cover_image] - The cover image of the room (optional).
 * @property {string} created_at - The created time of the message.
 */

/**
 * @enum {string}
 */
const WSChatMessageErrorType = {
	NOT_FOUND: 'user_not_found',
	NOT_FRIEND: 'not_friend',
	BLOCKED: 'blocked',
	BLOCKED_BY_OTHER: 'blocked_by_other',
};

/**
 * @typedef {Object} Profile
 * @property {string} username - The username of the profile.
 * @property {string} nickname - The nickname of the profile.
 * @property {string} avatar - The avatar url of the profile.
 * @property {User} user - The user of the profile.
 */

/**
 * @typedef {Object} User
 * @property {string} id - The id of the user.
 * @property {string} username - The username of the user.
 * @property {string} email - The email of the user.
 */

/**
 * @typedef {Object} ActiveChatRoom
 * @property {string} id - The ID of the active chat room.
 * @property {User} user - The user of the active chat room.
 * @property {ChatRoom} room - The ID of the room.
 * @property {Message} [last_message] - The last message of the active chat room.
 * @property {number} unread_count - The unread message count of the active chat room.
 */

/**
 * @typedef {Object} Message
 * @property {string} id - The ID of the message.
 * @property {Profile} sender - The sender profile of the message.
 * @property {string} message - The message content.
 * @property {string} created_at - The created time of the message.
 * @property {ChatRoom} room - The room of the message.
 */

/**
 * @typedef {Object} ChatRoom
 * @property {string} id - The ID of the room.
 * @property {string} name - The name of the room.
 * @property {string} cover_image - The cover image of the room.
 * @property {boolean} is_public - is the room public.
 * @property {boolean} is_group_chat - is the room a group chat.
 */
