$(init);
function init(){
	$('.t_input').each(function(){
		$(this).attr("placeholder", $(this).attr("name"));
		$(this).attr("onchange", "changeGroup($(this).val(), $(this).attr('name'))");
	});
}

function changeGroup(val, elename){
	$("input[name="+elename+"]").each(function(){
		$(this).val(val);
	});
}

