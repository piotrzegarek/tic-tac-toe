const socket = io({autoConnect: false});
let gameSessionId;

/**
 * Connect to socket on page load and create button click handlers.
 */
$(document).ready(function(){
    socket.connect();

    socket.on('connect-response', function(data) {
        if (data.success) {
            gameSessionId = data.game_session_id;
        } else {
            showError(data.error);
        }
    });
    buttonHandlers();
});

/**
 * Add click handlers to buttons.
 */
function buttonHandlers() {
    $("#addTickets").on( "click", function() {
        addTickets();
    });

    $("#startGame").on( "click", function() {
        startGame();
    });

    $("#exitSession").on( "click", function() {
        window.location.href = "/";
    });

    $(".board-square").on( "click", function() {
        selectSquare(this);
    });
}

/**
 * POST request to start game, if success then start socket connection.
 */
function startGame() {
    socket.emit('startGame', {game_session_id: gameSessionId});

    socket.on('startGame-response', function(data) {
        if (data.success) {
            $("#ticketCount").text(data.tickets);
            $("#startGame").fadeOut(200, function() {
                $(".board").fadeIn(200);
                $("#turnText").fadeIn(200);
            });
        } else {
            showError(data.error);
        }
    });
}

/**
 * POST request to add tickets to user, if success then update ticket count.
 */
function addTickets() {
    socket.emit('addTickets', {game_session_id: gameSessionId});

    socket.on('addTickets-response', function(data) {
        if (data.success) {
            $("#ticketCount").text(10);
        } else {
            showError(data.error);
        }
    });
}

function selectSquare(square) {
    // post for move, if success then update board
    if (true) {
        html = `<img src="../../../static/assets/images/x_black.png" class="board-square-img">`;
        $(square).html(html);
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