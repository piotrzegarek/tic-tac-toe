const socket = io({autoConnect: false});
let gameSessionId;
let gameId = null;
let player = null;
let turn = 'x';

/**
 * Connect to socket on page load and create button click handlers.
 */
$(document).ready(function(){
    socket.connect();
    buttonHandlers();
});

$(window).on('beforeunload', function(){
    if (gameId) {
        socket.emit('exitGame', {game_id: gameId});
    }
});

socket.on('connect-response', function(data) {
    if (data.success) {
        gameSessionId = data.game_session_id;
    } else {
        showError(data.error);
    }
});

/**
 * Add click handlers to buttons.
 */
function buttonHandlers() {
    $("#addTickets").on( "click", function() {
        socket.emit('addTickets', {game_session_id: gameSessionId});
    });

    $("#startGame").on( "click", function() {
        socket.emit('startGame', {game_session_id: gameSessionId});
    });

    $("#exitSession").on( "click", function() {
        if (gameId) {
            socket.emit('exitGame', {game_id: gameId});
        }
        window.location.href = "/";
    });

    $(".board-square").on( "click", function() {
        makeMove(this);
    });
}

/**
 * Emit startGame event to server, if success then update game id and show board.
 */
socket.on('startGame-response', function(data) {
    if (data.success) {
        gameId = data.game_id;
        player = data.player;
        $(".board-square").html("");
        $(".board").removeClass("game-over");
        handleTurn();
        $("#ticketCount").text(data.tickets);
        $("#startGame").fadeOut(200, function() {
            $(".board").fadeIn(200);
            $("#turnText").fadeIn(200);
        });
    } else {
        showError(data.error);
    }
});

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
 * Emit makeMove event to server.
 * @param {object} square - Square that was clicked.
 */
function makeMove(square) {
    var square_id = $(square).attr('id');
    socket.emit('makeMove', {square_id: parseInt(square_id), game_id: gameId, player: player});
}

/**
 * Handle makeMove-response event from server. If success then update board with move.
 * @param {object} data - Data from server.
 */
socket.on('makeMove-response', function(data) {
    if (data.success) {
        turn = data.turn;
        handleTurn();
        if (turn == 'o') {
            html = `<img src="../../../static/assets/images/x_black.png" class="board-square-img">`;
        } else {
            html = `<img src="../../../static/assets/images/o_black.png" class="board-square-img">`;
        }
        $(`#${data.square_id}`).html(html);
    } else {
        showError(data.error);
    }
});

socket.on('gameOver', function(data) {
    if (data.winner == player) {
        $("#gameResult").text("You win!");
    } else {
        $("#gameResult").text("You lose!");
    }
    $("#ticketCount").text(data.tickets);
    $(".board").addClass("game-over");
    $("#turnText").fadeOut(200, function() {
        $("#startGame").fadeIn(200);
        
    });
    gameId = null;
    player = null;
    turn = 'x';
});



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