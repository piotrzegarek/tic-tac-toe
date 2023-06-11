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
        $(".board-square").html("");
        renderBoard(data.board);
        gameId = data.game_id;
        player = data.player;
        turn = data.turn;
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
        renderBoard(data.board);
        socket.emit('waitForMove', {game_id: gameId, player: player});
    } else {
        showError(data.error);
    }
});

/**
 * Handle enemy move event from server and update board.
 */
socket.on('enemyMove-response', function(data) {
    if (data.success) {
        turn = data.turn;
        handleTurn();
        renderBoard(data.board);
    } else {
        showError(data.error);
    }
});
