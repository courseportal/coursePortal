$(init);

$("#previewform").nm();

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

	//create sortable
	$( '#questionsList' ).sortable({
		update: function(event, ui) {
	      $('#questionsList>.row-fluid').each(function(index){
	      	num = index+1;
	      	$(this).attr('id', 'question'+num)
	         $(this).find('.question-edit').attr('onclick', 'load_question('+num+')');
	         $(this).find('.question-remove').attr('onclick', 'remove_question('+num+')');
	      });
	   },
	});

	//init the dialog
	$( '#dialog' ).dialog({ 
		width: document.body.clientWidth*0.50,
		height: document.body.clientHeight*0.7,
		modal: true,
		autoOpen: false,
		open: function(event, ui){
			//codemirrors are always reconstructed so they animate correctly
			code = CodeMirror($('#codediv').get(0), CodeMirrorSettings);
			solution = CodeMirror($('#solndiv').get(0), CodeMirrorSettings);
			load_question_helper();
		},
		focus: function(event, ui){
			//disable parent scrolling
			$('body').addClass('dialog-open');
		},
		close: function(event, ui){
			//re-enable parent scrolling
			$('body').removeClass('dialog-open');
		},
		beforeClose: function( event, ui ) {
			// warning = 'Are you sure you want to cancel editing?  Any changes will not be saved.';
			// if(confirm(warning))
			// 	return true;
			// else
			// 	return false;
		},
		dialogClass: 'no-close',
	});
	//init wysiwyg
	tinymce.init({
	   selector: 'textarea#text',
	   force_p_newlines : false 
	});

	//initalize datepickers
	$('#assigndate').datepicker();
	$('#duedate').datepicker();

	$( '#opener' ).attr('onclick', "load_question($('#questionsList').children().length+1)");
}

function add_choice_div(){
	$('#choicediv').append('<div class="answer"></div>');
	choices.push(CodeMirror($('.answer:last').get(0), CodeMirrorSettings));
}

function load_question(num){ 
	$('#questionNum').val(num);
	//change save destination
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
			'<div class="row-fluid" id="question'+num+'"> \
				<input type="hidden"></input> \
				<div class="span5 question-description">'+
				$('#questiontitle').val()+
				'</div> \
				<div class="span1 btn question-edit" onclick="load_question('+num+')"> \
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
	datafield = $('#question'+num).find('input[type=hidden]');
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

	//kill codemirrors so that they can be replaced
	$('#codediv').html('');
	$('#solndiv').html('');

	//update the description
	$('#question'+num).find('.question-description').html(question.title);
}

function remove_question(num){
	if(confirm('Are you sure you want to delete this question?'))
		$('#question'+num).remove()
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

function preview(){
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

   $('#previewdata').val(JSON.stringify(assignment, undefined, 2));
   $('#previewform').submit();
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
