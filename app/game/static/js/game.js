$(document).ready(function(){
    buttonHandlers();
});

/**
 * End session before exit.
 */
$(window).bind('beforeunload', function(){
    // if game is running end game and session
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
        exitSession();
    });

    $(".board-square").on( "click", function() {
        selectSquare(this);
    });
}

/**
 * POST request to start game, if success then start socket connection.
 */
function startGame() {
    // post for game creation and socket connection
    $("#startGame").fadeOut(200, function() {
        $(".board").fadeIn(200);
        $("#turnText").fadeIn(200);
    });
}

/**
 * POST request to add tickets to user, if success then update ticket count.
 */
function addTickets() {
    // post for ticket addition, if success then update ticket count
    if (true) {
        $("#ticketCount").text(10);
    }
}

function selectSquare(square) {
    // post for move, if success then update board
    if (true) {
        html = `<img src="../../../static/assets/images/x_black.png" class="board-square-img">`;
        $(square).html(html);
    }
}

/**
 * POST request to end game and session, if success then redirect to home page.
 */
function exitSession() {
    // post for session exit, if success then redirect to home page
    if (true) {
        window.location.href = "/";
    }
}

