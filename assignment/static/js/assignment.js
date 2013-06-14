$(init);

CodeMirrorSettings = {
	mode: 'python',
	tabSize: 2,
	lineNumbers: true,
	indentWithTabs: true,
	theme: 'monokai'
};

code = {};
solution = {};
choices = [];
text = {};

function init(){
	$( '#questionsList' ).sortable({
		update: function(event, ui) {
	      $('#questionsList>.row-fluid').each(function(index){
	         $(this).find('.question-edit').attr('onclick', 'load_question('+index+')');
	         $(this).find('.question-remove').attr('onclick', 'remove_question('+index+')');
	      });
	   },
	});
	$( '#dialog' ).dialog({ 
		width: document.body.clientWidth*0.50,
		// maxWidth: document.body.clientWidth*0.8,
		height: document.body.clientHeight*0.7,
		// maxHeight: document.body.clientHeight*0.7,
		modal: true,
		autoOpen: false,
		open: function(event, ui){
			code = CodeMirror($('#codediv').get(0), CodeMirrorSettings);
			solution = CodeMirror($('#solndiv').get(0), CodeMirrorSettings);
			load_question_helper();
		},
		focus: function(event, ui){
			$('body').addClass('dialog-open');
		},
		close: function(event, ui){
			$('body').removeClass('dialog-open');
		},
		beforeClose: function( event, ui ) {
		},
	});
	tinymce.init({
	   selector: 'textarea#text',
	   force_p_newlines : false 
	});

	$('#assigndate').datepicker();
	$('#duedate').datepicker();

	$( '#opener' ).attr('onclick', "load_question($('#questionsList').children().length+1)");
}

function add_choice_div(){
	$('#choicediv').append('<div class="answer"></div>');
	choices.push(CodeMirror($('.answer:last').get(0), CodeMirrorSettings));
}

function load_question(num){ 
	//change save destination
	$('#questionNum').val(num);
	$('#question-save-button').attr('onclick', 'save_question('+num+')');
	$( '#dialog' ).dialog('open');
	//open the dialog
}

function load_question_helper(){
	num = $('#questionNum').val();
	numQuestions = $('#questionsList').children().length;
	if(num > numQuestions){ //this is a new question

		//wipe out all form fields
		$('#questiontitle').val('');
		code.setValue('');
		solution.setValue('');
		$('#choicediv').html(''); //wipe out choices
		choices = [];
		tinymce.activeEditor.setContent('');
	}

	else{
		//load the data from the text
		questiondata = $('#questionsList :nth-child('+num+')').find('input[type=hidden]').val();
		question = jQuery.parseJSON(questiondata);

		//replace the fields
		$('#questiontitle').val(question.title);
		code.setValue(question.code);
		solution.setValue(question.solution);
		$('#choicediv').html(''); //wipe out choices
		choices = [];
		for (var i = 0; i < question.choices.length; i++){//replace them
			$('#choicediv').append('<div class="answer"></div>');
			choices.push(CodeMirror($('.answer:last').get(0), CodeMirrorSettings));
			choices[i].setValue(question.choices[i]);
		}
		tinymce.activeEditor.setContent(question.text);
	}
}

function save_question(num){

	numQuestions = $('#questionsList').children().length;
	//if a new question, add to the question list
	if(num > numQuestions){
		questionHTML = 
			'<div class="row-fluid"> \
				<input type="hidden"></input> \
				<div class="span5 question-description">'+
				$('#questiontitle').val()+
				'</div> \
				<div class="span1 btn" onclick="load_question('+num+')"> \
					<i class="icon-edit-sign"> Edit</i> \
				</div> \
				<div class="span1 question-pts"> \
					<input type="text" class="input-fit" value="0"></input> \
				</div> \
				<div class="span1 question-remove btn" onclick="remove_question('+num+')"> \
					<i class="icon-remove-sign"></i> \
				</div> \
			</div>';
		$('#questionsList').append(questionHTML);
	}

	//create the question object
	datafield = $('#questionsList :nth-child('+num+')').find('input[type=hidden]');
	question = {
		choices: [],
	};
	question.title = $('#questiontitle').val();
	question.code = code.getValue();
	question.solution = solution.getValue();
	for(var i = 0; i < choices.length; i++){
		question.choices.push(choices[i].getValue());
	}
	question.text = tinymce.activeEditor.getContent();
	questiondata = JSON.stringify(question);
	datafield.val(questiondata);

	//close the dialog
	$( '#dialog' ).dialog('close');
	$('#codediv').html('');
	$('#solndiv').html('');
}

function remove_question(num){
	$('#questionsList :nth-child('+num+')').remove()
}

function remove_question_exists(userid, qid){
	name="#";
	name=name.concat(userid,'_', qid);
	$(name).remove();
}

function save(){
	//empty object
	assignment = {
		title: '',
		start: '',
		due: '',
		questions: [],		
	}

	assignment.title = $('#assigntitle').val();
	assignment.start = $('#assigndate').datepicker('getDate');
	assignment.due = $('#duedate').datepicker('getDate');



	$('#questionsList>.row-fluid').each(function(index){
		questiondata = $(this).find('input[type=hidden]').val();
		question = jQuery.parseJSON(questiondata);
		question.points = $(this).find('input[type=text]').val();
		console.log($(this).find('input[type=text]'))
		assignment.questions.push(question);
   });

   $('#assignmentdata').val(JSON.stringify(assignment, undefined, 2));
   $('#assignmentForm').submit();
}

// function add_question(){
// 	//wipe out the form
// 	$('#questiontitle').val('');
// 	code.setValue('');
// 	solution.setValue('');
// 	$('#choicediv').html('');
// 	tinymce.activeEditor.setContent('');

// 	//change save destination
// 	$('#question-save-button').attr('onclick', 'save_question(-1)');

// 	//open form
// 	$( '#dialog' ).dialog('open');
// }
