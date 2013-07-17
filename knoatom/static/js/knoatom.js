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
						var nametag = '.name-' + data.item + '-' + data.id;
						var sticktag = '.stickied-' + data.item + '-' + data.id;

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
	Delete object AJAX functionality
*/
init_delete_content = function() {
	$('.delete-content').click(function() {
		$.ajax({
			'url': '/ajax/delete/' + $(this).attr('item-type') + '/' + $(this).attr('item-id') + '/',
			'context': this,
			'statusCode' : {
				200: function(data) {
					console.log(data);
					if (data.result == true) {
						console.log(this);
						var row = '#row-' + data.item + '-' + data.id;
						$(row).remove();
						$("table").trigger("update");
						$('.cur-user-rate').text(data.user_rating);
					}
					else {
						alert("Failed to delete object!")
					}
				}
			},
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
    init_sidebar();
	init_sticking();
    init_video_viewer();
});
