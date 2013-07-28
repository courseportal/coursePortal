var vote_done = function(data) {
    if (data.result == true)
    {
        var vote_div = '#votes-sum-'+data.item+'-'+data.id;
        if (data.user_rating)
        {
            $('#cur-user-rate').text(data.user_rating);
        }
        $(vote_div).text(data.votes);
        $('table').trigger('update');
    }
    else
    {
        if (data.alert)
        {
            alert(data.alert);
        }
        else
        {
            alert('Voting failed!');
        }
    }
}

/*
 * Vote_up initialization
 */
init_vote_up = function() {
    $('.arrow-up').click(function() {
        $.ajax({
            url: '/vote/ajax/'+ $(this).attr('atom-id') + '/' + $(this).attr('item-type') + '/' + $(this).attr('item-id') + '/' + 'up' + '/',
            method: 'GET',
        }).success(vote_done);
        
    });
};

/*
 * Vote_down initialization
 */
init_vote_down = function() {
    $('.arrow-down').click(function() {
        $.ajax({
            url: '/vote/ajax/'+ $(this).attr('atom-id') + '/' + $(this).attr('item-type') + '/' + $(this).attr('item-id') + '/' + 'down' + '/',
            method: 'GET',
        }).success(vote_done);
    });
};

$(document).ready(function () {
    init_vote_up();
    init_vote_down();
})