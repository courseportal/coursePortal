
count = 1;
YUI_list = []
function add_text(){
	newdiv = '<textarea name="temp" id="temp"></textarea>';
	newdiv = newdiv.replace(/temp/g, 'text'+count);
	$('#alttextlistdiv').append(newdiv);
	render_YUI('text'+count,'60px');
	count++;
}
function add_choice(){
	choiceDivName = '<textarea name="temp" id="temp"> </textarea>';
	choiceDivName = choiceDivName.replace(/temp/g, 'choice'+count);
	$('#choicelistdiv').append(choiceDivName);
	render_YUI('choice'+count,'40px');
	count++;
}
function render_YUI(div, textheight){
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
	YUI_list.push(myEditor);
}
function hide_YUI_toolbar(div){
	$('#'+div+'_toolbar').css({
		'display':'none'
	});
}
render_YUI('solution');
render_YUI('text');

function save_YUI(){
	for (var i = 0; i < YUI_list.length; i++) {
  		YUI_list[i].saveHTML();
  	}
  	$('#questionForm').submit();
}