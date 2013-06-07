$(init);

// (function( $, undefined ) {
//   if ($.ui && $.ui.dialog) {
//     $.ui.dialog.overlay.events = $.map('focus,keydown,keypress'.split(','), function(event) { return event + '.dialog-overlay'; }).join(' ');
//   }
// }(jQuery));

function init(){
	$( '#questionsList2' ).sortable();
	$( '#dialog' ).dialog({ 
		width: document.body.clientWidth*0.7,
		// maxWidth: document.body.clientWidth*0.8,
		height: document.body.clientHeight*0.68,
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
	// $( '#dialog' ).load('assignment/question/form/')
	load_Form();
	$( '#opener' ).click(function() {
  		$( '#dialog' ).dialog("open");
	});
}

CodeMirrorSettings = {
	mode: 'python',
	tabSize: 2,
	lineNumbers: true,
	indentWithTabs: true,
	theme: 'monokai'
};

function add_choice(){
	newDiv = '<div id="temp" class="soln"></div>';
	newDiv = newDiv.replace(/temp/g, 'soln'+solnIndex);
	$('#solnDiv').append(newDiv);
	solutions.push(CodeMirror($('#soln'+solnIndex).get(0), CodeMirrorSettings));
	solnIndex++;
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

function load_Form(){
	tinymce.init({
	   selector: 'textarea#text',
	   force_p_newlines : false 
	});
	CodeMirror.fromTextArea($('#solution').get(0), CodeMirrorSettings);
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
