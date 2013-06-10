
CodeMirrorSettings = {
	mode: 'python',
	tabSize: 2,
	lineNumbers: true,
	indentWithTabs: true,
	theme: 'monokai',
	autofocus: false
};

tinymce.init({
   selector: 'textarea#text',
   force_p_newlines : false
});
CodeMirror.fromTextArea($('#solution').get(0), CodeMirrorSettings);