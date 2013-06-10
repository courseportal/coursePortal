$(init);

CodeMirrorSettings = {
	mode: 'python',
	tabSize: 2,
	lineNumbers: true,
	indentWithTabs: true,
	theme: 'monokai'
};

solutions = []

function init(){
	$( '#questionsList2' ).sortable();
	$( '#dialog' ).dialog({ 
		width: document.body.clientWidth*0.50,
		// maxWidth: document.body.clientWidth*0.8,
		height: document.body.clientHeight*0.8,
		// maxHeight: document.body.clientHeight*0.7,
		modal: true,
		autoOpen: false,
		focus: function(event, ui){
			$('body').addClass('dialog-open');
		},
		close: function(event, ui){
			$('body').removeClass('dialog-open');
		}
	});
	tinymce.init({
	   selector: 'textarea#text',
	   force_p_newlines : false 
	});
	CodeMirror.fromTextArea($('#codetext').get(0), CodeMirrorSettings);
	CodeMirror.fromTextArea($('#solntext').get(0), CodeMirrorSettings);

	$( '#opener' ).click(function() {
  		$( '#dialog' ).dialog("open");
	});
}

function add_choice_div(){
	newDiv = '<div class="answer"></div>';
	$('#choicediv').append(newDiv);
	solutions.push(CodeMirror($('#choicediv').get(0), CodeMirrorSettings));
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
	for (var i = 0; i < solutions.length; i++) {
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
