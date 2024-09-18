/**
 * @typedef {Object} CurrentUser
 * @property {string} id
 * @property {string} username
 * @property {string} email
 * @property {string} first_name
 * @property {string} last_name
 * @property {boolean} email_verified
 * @property {Profile} profile
 * @property {string} active_tournament_id
 */

/**
 * @typedef {Object} WSChatMessage
 * @property {WSChatMessageErrorType} [error]
 * @property {string} [type]
 * @property {string} message
 * @property {User} sender
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
 * @property {string} nickname
 * @property {string} bio
 * @property {string} avatar
 */

/**
 * @typedef {Object} User
 * @property {string} id
 * @property {string} username
 * @property {string} email
 * @property {Profile} profile
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
 * @property {User} sender
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
 * @property {User} owner
 * @property {TournamentPlayer[]} players
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
 * @property {TournamentMatchStatus} status
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
 * @property {TournamentRoom} tournament
 * @property {string} created_at
 */

/**
 * @enum {string}
 */
const TournamentStatus = {
	WAITING: 'W',
	ONGOING: 'O',
	COMPLETED: 'C',
};

/**
 * @enum {string}
 */
const TournamentMatchStatus = {
	WAITING: 'W',
	ONGOING: 'O',
	COMPLETED: 'C',
};

/**
 * @typedef {Object} WSTournamentMessage
 * @property {WSTournamentMessageType} type
 * @property {string} [user_id]
 * @property {string} tournament_id
 * @property {string} message
 */

/**
 * @enum {string}
 */
const WSTournamentMessageType = {
	PLAYER_JOINED: 'player_joined',
	PLAYER_LEFT: 'player_left',
	OWNER_LEFT: 'owner_left',
	PLAYER_REJOINED: 'player_rejoined',
	TOURNAMENT_STARTED: 'tournament_started',
	ERROR: 'error',
};
