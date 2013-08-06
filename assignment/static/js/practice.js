

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