const socket = io({autoConnect: false});
let gameSessionId;
let gameId = null;
let player = null;
let turn = null;

/**
 * Connect to socket on page load and create button click handlers.
 */
$(document).ready(function(){
    socket.connect();
    buttonHandlers();
});

/**
 * Exit game and remove game from the server on page unload.
 */
$(window).on('beforeunload', function(){
    if (gameId) {
        socket.emit('exitGame', {game_id: gameId});
    }
});

/**
 * Set game session id after connecting to socket.
 */
socket.on('connect-response', function(data) {
    if (data.success) {
        gameSessionId = data.game_session_id;
    } else {
        showError(data.error);
    }
});


/**
 * Render board after receiving board data from server.
 * @param {object} data - Board data.
 */
function renderBoard(board) {
    for (let i = 0; i < board.length; i++) {
        if (board[i] == 'x') {
            html = `<img src="../../../static/assets/images/x_black.png" class="board-square-img">`;
        } else if (board[i] == 'o') {
            html = `<img src="../../../static/assets/images/o_black.png" class="board-square-img circle">`;
        } else {
            html = ``;
        }
        $(`#${i}`).html(html);
    }
}


/**
 * End session and redirect to home page.
 */
socket.on('endSession', function(data) {
    $(".board").fadeOut(200);
    $("#turnText").fadeOut(200);
    $("#startGame").fadeOut(200);
    $("#errorSpan").text("Session ended");
    $("#errorSpan").addClass("show");
    setTimeout(function() {
        window.location.href = "/";
    }, 4000);
})

/**
 * Emit addTickets event to server, if success then update ticket count.
 */
socket.on('addTickets-response', function(data) {
    if (data.success) {
        $("#ticketCount").text(10);
    } else {
        showError(data.error);
    }
});


/**
 * Handle game over event from the server and show result.
 */
socket.on('gameOver', function(data) {
    if (data.winner == player) {
        $("#gameResult").text("You win!");
        $("#ticketCount").text(data.tickets);
    } else if (data.winner == 'draw') {
        $("#gameResult").text("Draw!");
    } else {
        $("#gameResult").text("You lose!");
    }
    $(".board").addClass("game-over");
    $("#turnText").fadeOut(200, function() {
        $("#startGame").fadeIn(200);
    });
    gameId = null;
    player = null;
    turn = null;
});


/**
 * Change turn text based on whose turn it is.
 */
function handleTurn() {
    if (turn == player) {
        $("#turnText").text("Your turn");
    } else {
        $("#turnText").text("Opponent's turn");
    }
}

/**
 * Show error message for 3 seconds.
 * @param {string} error - Error message to display.
 */
function showError(error) {
    $("#errorSpan").text(error);
    $("#errorSpan").addClass("show");
    setTimeout(function() {
        $("#errorSpan").removeClass("show");
    }, 3000);
}