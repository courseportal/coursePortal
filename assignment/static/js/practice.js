
$(init);

function init(){
	$('#submitreport').attr('onclick', "submitQbug()");
}

function evalPractice(){
	var student_answer='';
	var answer=$('#answer').val();
	data = $('#inputForm').serializeArray();
	for(x=0; x<data.length; x++){
		if(data[x].name == 'choice')
			student_answer = data[x].value;
	}
	if(student_answer == ''){
		alert("No answer provided");
		return false;
	}
	data = {
		status: answer==student_answer,
		qid: $('#qid').val(),
	};
	$.ajax('/assignment/utility/practiceEval/', {
		type: 'GET',
		async: true,
		data:data,
	});
	$('#submit').prop('disabled', true);
	if(data.status){
		$('#result').append('<div>Correct</div>');
	}
	else{
		$('#result').append('<div>Incorrect</div>');
	}
}

function submitQbug(){
	if($('#problemText').val() == ''){
		alert("Please provide a description.");
	}
	else{
		data = {
			text: $('#problemText').val(),
			id: $('#qid').attr('value'),
		};
		$.ajax('/assignment/utility/reportQ/', {
			type: 'GET',
			async: true,
			data: data,
		});
		$('#submitreport').attr('onclick', "$('#reportform').modal('hide');");
		$('#reportform').modal('hide');
	}
}

$(document).ajaxError(function(event, request, settings) {
  alert( "Error requesting page " + request.responseText);
});