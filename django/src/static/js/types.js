/**
 * @typedef {Object} WSChatMessage
 * @property {WSChatMessageErrorType} [error]
 * @property {string} [type]
 * @property {string} message
 * @property {Profile} sender
 * @property {string} room_id
 * @property {string} room_name
 * @property {string} [cover_image]
 * @property {string} created_at
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
 * @property {string} username
 * @property {string} nickname
 * @property {string} avatar
 * @property {User} user
 */

/**
 * @typedef {Object} User
 * @property {string} id
 * @property {string} username
 * @property {string} email
 */

/**
 * @typedef {Object} ActiveChatRoom
 * @property {string} id
 * @property {User} user
 * @property {ChatRoom} room
 * @property {Message} [last_message]
 * @property {number} unread_count
 */

/**
 * @typedef {Object} Message
 * @property {string} id
 * @property {Profile} sender
 * @property {string} message
 * @property {string} created_at
 * @property {ChatRoom} room
 */

/**
 * @typedef {Object} ChatRoom
 * @property {string} id
 * @property {string} name
 * @property {string} cover_image
 * @property {boolean} is_public
 * @property {boolean} is_group_chat
 */

/**
 * @typedef {Object} TournamentRoom
 * @property {string} id
 * @property {string} name
 * @property {string} description
 * @property {Player} owner
 * @property {Player[]} players
 * @property {Player} [winner]
 * @property {TournamentMatch[]} [matches]
 * @property {TournamentStatus} status
 * @property {string} created_at
 * @property {string} ended_at
 */

/**
 * @typedef {Object} Player
 * @property {string} id
 * @property {User} user
 * @property {number} wins
 * @property {number} loses
 * @property {number} elo
 */

/**
 * @typedef {Object} TournamentMatch
 * @property {string} id
 * @property {TournamentPlayer} winner
 * @property {TournamentPlayer} loser
 * @property {number} winner_score
 * @property {number} loser_score
 * @property {TournamentRoom} tournament
 * @property {string} created_at
 */

/**
 * @typedef {Object} TournamentPlayer
 * @property {string} id
 * @property {Player} player
 * @property {number} position
 * @property {TournamentRoom} tournament
 */

/**
 * @enum {string}
 */
const TournamentStatus = {
	WAITING: 'W',
	ONGOING: 'O',
	COMPLETED: 'C',
};
