/*
 * Vote_up initialization
 */
init_vote_up = function() {
    $('.arrow-up').click(function() {
		$.ajax({
			'url': '/vote/ajax/' + $(this).attr('item-type')  + '/' + $(this).attr('vote-example-id') + '/' +  $(this).attr('vote-type'),
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
					}
					else {
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
			'url': '/vote/ajax/'+ $(this).attr('item-type') + '/' + $(this).attr('vote-example-id') + '/' +  $(this).attr('vote-type'),
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
					}
					else {
						alert("You have already voted!");
					}
				}
			}
		});
	});
};

$(document).ready(function () {
    init_vote_up();
    init_vote_down();
}