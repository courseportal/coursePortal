
count = 1;
solutions = [];
texts = [];
function add_text(){
	newdiv = '<textarea name="temp" id="temp"></textarea>';
	newdiv = newdiv.replace(/temp/g, 'text'+count);
	$('#alttextlistdiv').append(newdiv);
	render_YUI('text'+count, texts, '60px');
	count++;
}
function add_choice(){
	choiceDivName = '<textarea name="temp" id="temp"> </textarea>';
	choiceDivName = choiceDivName.replace(/temp/g, 'choice'+count);
	$('#choicelistdiv').append(choiceDivName);
	render_YUI('choice'+count, solutions, '40px');
	count++;
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
	group.push(myEditor);
}
render_YUI('solution', solutions);
render_YUI('text', texts);

function save_YUI(){
	question = {
		title: '',
		solutions: [],
		texts: []
	};
	$('#questionname').val($('#title').val());
	question.title = $('#title').val();
	for (var i = 0; i < solutions.length; i++) {
  		question.solutions.push(solutions[i].saveHTML());
  	}
  	for (var i = 0; i < texts.length; i++) {
  		question.texts.push(texts[i].saveHTML());
  	}
  	$('#data').val(JSON.stringify(question));
  	$('#questionForm').submit();
}