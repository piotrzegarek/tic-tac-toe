/**
 * Add click handlers to buttons.
 */
function buttonHandlers() {
    $("#addTickets").on( "click", function() {
        socket.emit('addTickets', {game_session_id: gameSessionId});
    });

    $("#startGame").on( "click", function() {
        socket.emit('startGame-multiplayer', {game_session_id: gameSessionId});
    });

    $("#exitSession").on( "click", function() {
        if (gameId) {
            socket.emit('exitGame', {game_id: gameId, player: player});
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
            $("#ticketCount").text(data.tickets);
        }
        if (data.oponent) {
            $(".board-square").html("");
            $(".board").removeClass("game-over");
            handleTurn();
            if (data.oponent == player) {
                $("#ticketCount").text(data.tickets);
            }
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
        showError(data.error);
    }
});


/**
 * Emit makeMove event to server.
 * @param {object} square - Square that was clicked.
 */
function makeMove(square) {
    var square_id = $(square).attr('id');
    socket.emit('makeMove-multiplayer', {square_id: parseInt(square_id), game_id: gameId, player: player});
}


/**
 * Handle makeMove-response event from server. If success then update board with move.
 * @param {object} data - Data from server.
 */
socket.on('makeMove-response', function(data) {
    if (data.success) {
        turn = data.turn;
        handleTurn();
        renderBoard(data.board);
    } else {
        showError(data.error);
    }
});


/**
 * Handle game over event from the server and show result.
 */
socket.on('gameOver-multiplayer', function(data) {
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
    socket.emit('leaveRoom', {game_id: gameId});
    gameId = null;
    player = null;
    turn = null;
});


socket.on('exitGame-response', function(data) {
    $("#ticketCount").text(data.tickets);
    $("#gameResult").text("You win!");
    $("#turnText").fadeOut(200, function() {
        $('#startGame').fadeIn(200);
    });
    $(".board").addClass("game-over");
    socket.emit('leaveRoom', {game_id: gameId});
    gameId = null;
    player = null;
    turn = null;
});