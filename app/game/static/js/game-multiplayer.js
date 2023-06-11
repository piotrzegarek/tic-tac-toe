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
        console.log(gameId, player, turn);
        socket.emit('addTickets', {game_session_id: gameSessionId});
    });

    $("#startGame").on( "click", function() {
        socket.emit('startGame-multiplayer', {game_session_id: gameSessionId});
        console.log("startGame-multiplayer");
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
        turn = data.turn;
        if (player == null) {
            player = data.player;
        }
        if (data.oponent) {
            $(".board-square").html("");
            $(".board").removeClass("game-over");
            handleTurn();
            $("#ticketCount").text(data.tickets);
            $("#startGame").fadeOut(200, function() {
                $(".board").fadeIn(200);
                $("#turnText").fadeIn(200);
            });
        } else {
            $("#turnText").text(`Waiting for oponent...`);
            $("#startGame").fadeOut(200, function() {
                $("#turnText").fadeIn(200);
            });
        }
    } else {
        // showError(data.error);
    }
});

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


function handleTurn() {
    if (turn == player) {
        $("#turnText").text(`${turn} turn`);
    } else {
        $("#turnText").text(`${turn} turn`);
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