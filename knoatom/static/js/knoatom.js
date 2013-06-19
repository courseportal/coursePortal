/*
 * Sidebar initialization
 */
init_sidebar = function() {
    $('.sidebar-dropdown-toggle').click(function() {
        if(!$(this).parent().next().is(":visible"))
            $(this).removeClass('icon-plus').addClass('icon-minus');
        else
            $(this).removeClass('icon-minus').addClass('icon-plus');
        $(this).parent().next().toggle('slow');
        return false;
    });
    $('.sidebar-dropdown-toggle').each(function() {
        if(!$(this).parent().parent().hasClass('open')) {
            $(this).parent().next().hide();
            $(this).removeClass('icon-minus').addClass('icon-plus');
        }
    });
};

/*
 * Rating stars initialization
 */
init_rating_stars = function() {
    $('.rating').each(function() {
        $(this).children().each(function() {
            $(this).hover(function() {
                $(this).addClass('icon-star')
                    .removeClass('icon-star-empty')
                    .prevAll()
                    .addClass('icon-star')
                    .removeClass('icon-star-empty');
                $(this).nextAll()
                    .addClass('icon-star-empty')
                    .removeClass('icon-star');
            }, function() {
                $(this).parent().children().each(function() {
                    if(!$(this).hasClass('filled')) {
                        $(this).removeClass('icon-star').addClass('icon-star-empty')
                    } else {
                        $(this).removeClass('icon-star-empty').addClass('icon-star')
                    }
                });
            });
            $(this).click(function() {
                $.ajax({
                    'url': '/ajax/vote/' + $(this).parent().attr('data-submission') + '/' + $(this).parent().attr('data-vote-category') + '/' + $(this).attr('data-vote'),
                    'context': this,
                    'statusCode': {
                        200: function(data) {
                            console.log(data)
                            if(data.result == true) {
                                console.log(this)
                                $(this)
                                    .addClass('icon-star')
                                    .removeClass('icon-star-empty')
                                    .addClass('filled')
                                $(this).prevAll()
                                    .addClass('icon-star')
                                    .removeClass('icon-star-empty')
                                    .addClass('filled')
                                $(this).nextAll()
                                    .addClass('icon-star-empty')
                                    .removeClass('icon-star')
                                    .removeClass('filled')
                            }
                        }
                    },
                });
            });
        });
    });
};

/*
	Sticking AJAX funcitonality
*/
init_sticking = function() {
	$('.sticky').click(function() {
		$.ajax({
			'url': '/ajax/sticking/' + $(this).attr('class-id') + '/' + $(this).attr('item-type') + '/' + $(this).attr('item-id') + '/',
			'context': this,
			'statusCode': {
				200: function(data) {
					console.log(data)
					if(data.result == true) {
						console.log(this)
						var nametag = '.name-' + data.itemType + '-' + data.id;
						var sticktag = '.stickied-' + data.itemType + '-' + data.id;

						if (data.stickied) {
							$(nametag).text(data.name + ' [stickied]');
							$(sticktag).text(1)
						}
						else
						{
							$(nametag).text(data.name);
							$(sticktag).text(0)
						}
						$("table").trigger("update");
					}
					else
					{
						alert("Sticking or Unsticking this content failed.")
					}
				}
			}
		});
	});
	
	
};

/*
 * Vote_up initialization
 */
init_vote_up = function() {
    $('.arrow-up').click(function() {
                         
                         $.ajax({
                                'url': '/ajax/voteGeneral/' + $(this).attr('item-type')  + '/' + $(this).attr('vote-example-id') + '/' +  $(this).attr('vote-type'),
                                'context': this,
                                'statusCode': {
                                200: function(data) {
                                console.log(data)
                                if(data.result == true) {
                                console.log(this);
                                var s = '.votes-sum-'+data.itemType+'-'+data.id;
                                $('.cur-user-rate').text(data.requestUserRating);
                                $(s).text(data.votes);
								$("table").trigger("update");
                                }else{
                                alert("You have already voted!");
                                }
                                }
                                }
                                });
                         
                         
                         });
};

/*
 * Vote_down initialization
 */
init_vote_down = function() {
    $('.arrow-down').click(function() {
                         
                         $.ajax({
                                'url': '/ajax/voteGeneral/'+ $(this).attr('item-type') + '/' + $(this).attr('vote-example-id') + '/' +  $(this).attr('vote-type'),
                                'context': this,
                                'statusCode': {
                                200: function(data) {
                                console.log(data)
                                if(data.result == true) {
                                console.log(this);
                                var s = '.votes-sum-'+data.itemType+'-'+data.id;
                                $('.cur-user-rate').text(data.requestUserRating);
                                $(s).text(data.votes);
								$("table").trigger("update");
                                }else{
                                alert("You have already voted!");
                                }
                                }
                                }
                                });
                         
                         
                         });
};






/*
 * Video viewer on submissions
 */
init_video_viewer = function() {
    $('.view_video').each(function() {
        $(this).click(function(e) {
            e.preventDefault();
            var sid = $(this).parent().attr('data-sid');
            var vid = $(this).parent().attr('data-vid');
            var params = { allowScriptAccess: 'always' };
            var atts = { id: 'video_player_' + sid, 'wmode': 'opaque' };
            $('#video_player_' + sid).remove();
            $(this).parent().parent().parent().prepend('<div id="video_view_' + sid + '"></div>');
            $('#hide_video_' + sid).show();
            swfobject.embedSWF("http://www.youtube.com/v/" + vid + "?version=3&enablejsapi=1&playerapiid=player1", "video_view_" + sid, "560", "315", "9", null, null, params, atts);
        });
    });
    $('.hide_video').click(function() {
        var sid = $(this).attr('data-hide_sid');
        $('#hide_video_' + sid).hide();
        $('#video_player_' + sid).remove();
    });
};

/*
 * Call all the initialization functions
 */
$(document).ready(function() {
	init_sticking();
    init_sidebar();
    init_rating_stars();
    init_vote_up();
    init_vote_down();
    init_video_viewer();
});
