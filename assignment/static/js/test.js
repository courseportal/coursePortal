
CodeMirrorSettings = {
	mode: 'python',
	tabSize: 2,
	lineNumbers: true,
	indentWithTabs: true,
	theme: 'monokai'
};
// render_YUI('solution', solutions);
// render_YUI('text', texts);

code = CodeMirror.fromTextArea($('#solution').get(0), CodeMirrorSettings);
solutions = [];
// text = render_YUI('text');

tinymce.init({
   selector: "textarea#text",
   force_p_newlines : false
});

// function add_text(){
// 	newdiv = '<textarea name="temp" id="temp"></textarea>';
// 	newdiv = newdiv.replace(/temp/g, 'text'+count);
// 	$('#alttextlistdiv').append(newdiv);
// 	render_YUI('text'+count, texts, '60px');
// 	count++;
// }

solnIndex = 0;

function add_choice(){
	newDiv = '<div id="temp" class="soln"></div>';
	newDiv = newDiv.replace(/temp/g, 'soln'+solnIndex);
	$('#solnDiv').append(newDiv);
	solutions.push(CodeMirror($('#soln'+solnIndex).get(0), CodeMirrorSettings));
	solnIndex++;
}

function render_YUI(div, group, textheight){
	textheight = textheight || "100px";
	var myEditor = new YAHOO.widget.Editor(div, {
	    height: textheight,
	    width: $('#div').width(),
	    dompath: false,
	    animate: true,
	    toolbar: {
	        buttons: [
	            { group: 'textstyle', label: 'Font Style',
	                buttons: [
	                    { type: 'push', label: 'Bold', value: 'bold' },
	                    { type: 'push', label: 'Italic', value: 'italic' },
	                    { type: 'push', label: 'Underline', value: 'underline' },
	                    { type: 'separator' },
	                ]
	            }
	        ]
	    }
	});
	myEditor.render();
	return myEditor;
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