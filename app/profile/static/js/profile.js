$(document).ready(function() {
    $.post({
        url: '/profile/get_games.json',
        success: function(data) {
            renderTable(data);
        },
        error: function() {
            alert('Error');
        }
    })
});

function renderTable(data) {
    console.log(data);
    var table = $('#tableBody');
    var html = '';
    for (var [key, value] of Object.entries(data)) {
        html +=  `
        <tr>
          <td>${key}</td>
          <td>${value.games_count}</td>
          <td>${value.wins}</td>
          <td>${value.losses}</td>
          <td>${value.draws}</td>
        </tr>
        `
    }
    table.html(html);
};