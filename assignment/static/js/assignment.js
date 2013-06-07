$(init);

function init(){
	$("#formiframe").width ( $("#myModal").width()*0.98);
	$("#formiframe").height (document.body.clientHeight*0.5);
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

function loadForm(){
	TINY.box.show({
		iframe:'assignment/question/form/',
		close: true,
		boxid:'frameless',
		width:750,
		height:450,
		fixed:true,
		maskid:'blackmask',
		maskopacity:40,
		closejs: function(){
			closeJS()
		}
	});
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
