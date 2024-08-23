import { Paddle } from './classes/paddle.js';
import { Ball } from './classes/ball.js';
import { Table } from './classes/table.js';

// Client-side game setup and rendering
const gameCanvas = document.getElementById('gameCanvas');
const matchmaking = document.getElementById('matchmaking');
const scoreBoard = document.getElementById('scoreBoard');

const paddle1 = new Paddle(20, 200, 10, 100, 'white', 10);
const paddle2 = new Paddle(gameCanvas.width - 30, gameCanvas.height - 300, 10, 100, 'white', 10);
const ball = new Ball(gameCanvas.width / 2, gameCanvas.height / 2, 8, 'lightblue', 'lightblue', 5);
const table = new Table(gameCanvas, paddle1, paddle2, ball);

const socket = new WebSocket(`ws://${window.location.host}/ws/pong/${roomName}/`);
let assignedPaddle = null;

scoreBoard.style.display = 'none'
gameCanvas.style.display = 'none';
matchmaking.style.display = 'block';

socket.onopen = function() {
    console.log("WebSocket connection established " + roomName);
};
socket.onerror = function(error) {
    console.error("WebSocket error:", error);
};
socket.onclose = function(event) {
    console.log("WebSocket connection closed:", event);
};

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // console.log("Raw message data:", e.data);
    // console.log("Parsed data:", data);

    // if (data.type) {
    //     console.log("Message type:", data.type);
    // } else {
    //     console.error("Message type is undefined");
    // }

    if (data.type === 'player_assignment') {
        // Store the assigned paddle
        assignedPaddle = data.player;
    }
    if (data.type === 'start_game') {
        // Both players has connected, start the game
        matchmaking.style.display = 'none';
        gameCanvas.style.display = 'block';
        scoreBoard.style.display = 'block';
    }
    if (data.type === 'update_game_state') {
        // Update the game state based on the server's response
        paddle1.y = data.paddle1.y;
        paddle2.y = data.paddle2.y;
        ball.x = data.ball.x;
        ball.y = data.ball.y;
        document.getElementById('score1').innerText = data.score1;
        document.getElementById('score2').innerText = data.score2;

        // Render the updated game state
        table.draw();
    }
};

// Client Paddle Controls
document.addEventListener('keydown', (event) => {
    let velocity = null;

    if (event.key === 'w') {
        velocity = -10;
    } else if (event.key === 's') {
        velocity = 10;
    }

    if (velocity !== null) {
        socket.send(JSON.stringify({ 'paddle': assignedPaddle, 'velocity': velocity }));
    }
});

document.addEventListener('keyup', (event) => {
    if (event.key === 'w' || event.key === 's') {
        socket.send(JSON.stringify({ 'paddle': assignedPaddle, 'velocity': 0 }));
    }
});

// Game table object handling the rendering
table.draw = function() {
    this.clearBoard();
    this.paddle1.draw(this.ctx);
    this.paddle2.draw(this.ctx);
    this.ball.draw(this.ctx);
};



// let form = document.getElementById('form')
// form.addEventListener('submit', (e)=> {
//     e.preventDefault()
//     let message = e.target.message.value
//     socket.send(JSON.stringify({
//         'message':message
//     }))
//     form.reset()
// })

// let assignedPaddle = null;

// socket.onmessage = function(e) {
//     const data = JSON.parse(e.data);
//     console.log('Data:', data)

//     if (data.type === 'chat'){
//         let messages = document.getElementById('messages')

//         messages.insertAdjacentHTML('beforeend', `<div>
//                                 <p>${data.message}</p>
//                             </div>`)
//     }

//     if (data.player) {
//         // Assign the paddle to the client
//         assignedPaddle = data.player;
//     } else {
//         const paddle = data['paddle'];
//         const velocity = data['velocity'];

//         if (paddle === 'paddle1') {
//             paddle1.velocity = velocity;
//         } else if (paddle === 'paddle2') {
//             paddle2.velocity = velocity;
//         }
//     }
// };
