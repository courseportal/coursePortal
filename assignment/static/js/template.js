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

function validateSubmit(){
	formdata = $("#templateForm").serializeArray();
	for(var x=0; x<formdata.length; x++){
		if(formdata[x].value == null || formdata[x].value == ''){
			alert("Input field "+formdata[x].name+" is empty!");
			return false;
		}
	}
	$("#templateForm").submit();
}

