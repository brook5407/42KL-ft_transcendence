import { Paddle } from './classes/paddle.js';
import { Ball } from './classes/ball.js';
import { Table } from './classes/table.js';

// Client-side game setup and rendering
const container = document.getElementById('container');
const gameCanvas = document.getElementById('gameCanvas');
const score1 = document.getElementById('score1');
const score2 = document.getElementById('score2');
const canvasContainer = document.getElementById('canvasContainer');
const overlay = document.getElementById('overlay');
const countdownText = document.getElementById('countdownText');
const winnerText = document.getElementById('winnerText');
const matchmaking = document.getElementById('matchmaking');
const roomCode = document.getElementById('roomCode');

let paddle1;
let paddle2;
let ball;
let table;
let assignedPaddle = null;

const socket = new WebSocket(`ws://${window.location.host}/ws/${gameMode}/${roomName}/`);
roomCode.innerHTML = roomName;



socket.onopen = function() {
    console.log("WebSocket connection established " + roomName);
    socket.send(JSON.stringify({ 'game_mode': gameMode}));
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

    if (data.type === 'paddle_assignment') {
        // Store the assigned paddle
        console.log("paddle_assignment: " + data.paddle);
        assignedPaddle = data.paddle;

    }
    if (data.type === 'start_game') {
        // Both players has connected, start the game
        console.log("start_game");
        canvasContainer.height = data.gameHeight;
        canvasContainer.width = data.gameWidth;
        gameCanvas.height = data.gameHeight;
        gameCanvas.width = data.gameWidth;
        paddle1 = new Paddle(data.paddle1.x, data.paddle1.y, data.paddle1.width, data.paddle1.height, 'white');
        paddle2 = new Paddle(data.paddle2.x, data.paddle2.y, data.paddle2.width, data.paddle2.height, 'white');
        ball = new Ball(gameCanvas.width / 2, gameCanvas.height / 2, data.ball.radius, data.ball.speed, '#ffffff', '#A0D8F0');
        table = new Table(gameCanvas, paddle1, paddle2, ball);
        matchmaking.style.display = 'none';
        container.style.display = 'flex';
        if (assignedPaddle === 'paddle1') {
            paddle1.color = "#4FCDF0";
            score1.style.color = "#4FCDF0";
            paddle2.color = "#EC4242";
            score2.style.color = "#EC4242";
        } else if (assignedPaddle === 'paddle2') {
            paddle1.color = "#EC4242";
            score1.style.color = "#EC4242";
            paddle2.color = "#4FCDF0";
            score2.style.color = "#4FCDF0";
        }
    }
    if (data.type === 'countdown_game') {
        console.log("countdown_game");
        const countdownValue = data.message;
        countdownText.style.display = 'block';
        countdownText.innerHTML = countdownValue;

        if (countdownValue === 1) {
            setTimeout(() => {
                countdownText.innerHTML = 'Go!';
            }, 1000);  
            setTimeout(() => {
                countdownText.style.display = 'none';
                overlay.style.display = 'none';
            }, 2000);
        }
        table.draw();
    }
    if (data.type === 'update_game_state') {
        console.log("update_game_state");
        // Update the game state based on the server's response
        paddle1.y = data.paddle1.y;
        paddle2.y = data.paddle2.y;
        ball.x = data.ball.x;
        ball.y = data.ball.y;
        score1.innerText = data.score1;
        score2.innerText = data.score2;

        // Render the updated game state
        table.draw();
    }
    if (data.type === 'end_game') {
        console.log("end_game");
        // alert(data.message);

        // Make the darker overlay and text visible
        overlay.style.display = 'flex';
        winnerText.style.display = 'flex';
        winnerText.innerText = data.message;

        // Countdown back to main menu
        let countdown = 11;
        const countdownInterval = setInterval(() => {
            countdown -= 1;
            countdownText.style.fontSize = "12px";
            countdownText.innerText = `Returning to the main menu in ${countdown} seconds...`;
            countdownText.style.display = 'flex';
    
            if (countdown === 0) {
                clearInterval(countdownInterval);
                // socket.close();
                // window.location.href = `http://${window.location.host}/`;
            }
        }, 1000);
    }
    if (data.type === 'next_match') {
        overlay.style.display = 'flex';
        winnerText.style.display = 'flex';
        winnerText.innerText = data.message;

        let countdown = 11;
        const countdownInterval = setInterval(() => {
            countdown -= 1;
            countdownText.style.fontSize = "12px";
            countdownText.innerText = `Next match starting in ${countdown} seconds...`;
            countdownText.style.display = 'flex';
    
            if (countdown === 0) {
                clearInterval(countdownInterval);
                socket.send(JSON.stringify({ 'next_match': true}));
            }
        }, 1000);
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