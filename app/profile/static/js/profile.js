$(document).ready(function() {
    $('#datepicker').datepicker();
    getGamesData();

    $('#datepicker').on('change', function() {
        getGamesData();
    });
});


function getGamesData() {
    console.log($('#dateInput').val());
    $.ajax({
        url: '/profile/get_games.json',
        type: 'POST',
        data: JSON.stringify({
            'date': $('#dateInput').val()
        }),
        contentType: 'application/json;charset=UTF-8',
        success: function(data) {
            renderTable(data);
        },
        error: function() {
            alert('Error');
        }
    });
}

function renderTable(data) {
    var table = $('#tableBody');
    var html = '';
    for (var [key, value] of Object.entries(data)) {
        html +=  `
        <tr id='session-${key}' class='session-data'>
          <td>${key}</td>
          <td>${value.games_count}</td>
          <td>${value.wins}</td>
          <td>${value.losses}</td>
          <td>${value.draws}</td>
        </tr>
        <tr id='games-${key}' class='games-data hide'>
            <td colspan="5">
                <table class="table mb-0">
                    <thead>
                        <tr>
                            <th>Game No.</th>
                            <th>Result</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        for (var [key, value] of Object.entries(value.games)) {
            game_time = formatSecondsToMinutes(value.game_time);
            html += `
            <tr>
                <td>${parseInt(key)+1}</td>
                <td>${value.game_result}</td>
                <td>${game_time}</td>
            </tr>
            `;
        }
        html += `
                    </tbody>
                </table>
            </td>
        </tr>
        `
    }
    table.html(html);
    $('.session-data').on('click', function() {
        var id = $(this).attr('id').split('-')[1];
        $('#games-'+id).toggleClass('hide');
    });
};

function formatSecondsToMinutes(seconds) {
    var minutes = Math.floor(seconds / 60);
    var seconds = seconds - minutes * 60;
    return minutes + ':' + seconds + ' min';
}