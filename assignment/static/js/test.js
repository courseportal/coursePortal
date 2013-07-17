
//this is ajax CSRF certificate stuff.  ignore
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

CodeMirrorSettings = {
	mode: 'python',
	tabSize: 3,
	lineNumbers: true,
	indentWithTabs: true,
  theme: 'solarized',
};

code = CodeMirror.fromTextArea($('#solution').get(0), CodeMirrorSettings);
solutions = [];

tinymce.init({
   selector: "textarea#text",
   force_p_newlines : false
});

solnIndex = 0;
add_choice();

$(document).ready(function(){
	$('#previewform').dialog({
		width: document.body.clientWidth*0.8,
		height: document.body.clientHeight*0.7,
		modal: true,
		autoOpen: false,
	});
});


function add_choice(){
	newDiv = '<div id="temp" class="soln" style="border:solid"></div>';
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
		solution: {},
		choices: [],
		text: ''
	};
	question.title = $('#title').val();
	question.code = code.getValue();
	question.solution = solutions[0].getValue();
	for (var i = 1; i < solutions.length; i++) {
  	question.choices.push(solutions[i].getValue());
  }
  question.text = tinymce.activeEditor.getContent({format : 'raw'});

	$('#questionname').val($('#title').val());
  $('#data').val(JSON.stringify(question));
  $('#questionForm').submit();
}

function preview(){
	question = {
		title: '',
		code: '',
		solution: {},
		choices: [],
		text: ''
	};

	question.title = $('#title').attr('value');
	question.code = code.getValue();
	question.solution=solutions[0].getValue();
	for (var i = 1; i < solutions.length; i++) {
  		question.choices.push(solutions[i].getValue());
  	}
  	question.text = tinymce.activeEditor.getContent({format : 'raw'});

  	data={
  		previewname:$('#title').attr('value'),
  		previewdata:JSON.stringify(question),
  	};
  	$('#previewform').load('question/preview/', data, function(response, status, xhr){
   	if (status == "error") {
    		var msg = "Sorry but there was an error: ";
    		$("#previewform").html(msg + xhr.status + " " + xhr.statusText);
  		}
   });
   $('#previewform').dialog('open');
}