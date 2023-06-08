$(document).ready(function(){
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
}

/**
 * POST request to start game, if success then start socket connection.
 */
function startGame() {
    // post for game creation and socket connection
    $("#startGame").fadeOut(200, function() {
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