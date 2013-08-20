var vote_done = function(data) {
    if (data.result == true)
    {
        var vote_div = '#votes-sum-'+data.item+'-'+data.id;
        //var vote_up_div = '#votes-sum-up-'+data.item+'-'+data.id;
        //var vote_down_div = '#votes-sum-down-'+data.item+'-'+data.id;
        var vote_up_bar_div = '#sparkbar-likes-'+data.item+'-'+data.id;
        var vote_down_bar_div = '#sparkbar-dislikes-'+data.item+'-'+data.id;
        if (data.user_rating)
        {
            $('#cur-user-rate').text(data.user_rating);
        }
        $(vote_div).text(data.votes);
        //$(vote_up_div).text(data.votesUp);
        //$(vote_down_div).text(data.votesDown);
        var up=data.votesUp/(data.votesUp + data.votesDown)*100+"%";
        
        var down=data.votesDown/(data.votesUp + data.votesDown)*100+"%";
        
        $(vote_up_bar_div).css('width', up);
        
        if (data.votesUp !=0)
        {
            $(vote_up_bar_div).text(data.votesUp);
        }
        else
        {
            $(vote_up_bar_div).text('');
        }
        $(vote_down_bar_div).css('width', down);
        
        if (data.votesDown !=0)
        {
            $(vote_down_bar_div).text(data.votesDown);
        }
        else
        {
            $(vote_down_bar_div).text('');
        }
        
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