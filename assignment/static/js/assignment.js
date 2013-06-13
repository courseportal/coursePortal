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
	code = CodeMirror.fromTextArea($('#codetext').get(0), CodeMirrorSettings);
	solution = CodeMirror.fromTextArea($('#solntext').get(0), CodeMirrorSettings);

	$( '#opener' ).click(function() {
  		$( '#dialog' ).dialog("open");
	});
}

function add_choice_div(){
	$('#choicediv').append('<div class="answer"></div>');
	choices.push(CodeMirror($('.answer:last').get(0), CodeMirrorSettings));
}

function load_question(num){ 
	//wipe out existing data
	code.setValue('');
	solution.setValue('');
}

function save_question(num){

	if(num < 0){ //this is a new question

	}
}


function save(){
	//empty object
	question = {
		title: '',
		code: '',
		solutions: [],
		text: ''
	};

	question.title = $('#title').val();
	question.code = code.getValue();
	for (var i = 0; i < question.solutions.length; i++) {
  		question.solutions.push(solutions[i].getValue());
  	}
  	question.text = tinymce.activeEditor.getContent({format : 'raw'});

	$('#questionname').val($('#title').val());
  	$('#data').val(JSON.stringify(question));
  	$('#questionForm').submit();
}

$('#myModal').on('show', function () {
  $('body').addClass('dialog-open');
})

$('#myModal').on('hidden', function () {
  $('body').removeClass('dialog-open');
})

function add_question(){
	$('#myModal').modal('toggle');
}
