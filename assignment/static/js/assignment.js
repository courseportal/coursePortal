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
preview = {};


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
		height: document.body.clientHeight*0.5,
		overflow: scroll,
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
			warning = "Closing this will not save changes. Proceed?";
			if ( event.originalEvent && $(event.originalEvent.target).closest(".ui-dialog-titlebar-close").length ) {
				if(confirm(warning)){
					$('#codediv').html('');
					$('#solndiv').html('');
					return true;
				}
				else
					return false;
			}
			else{
				$('#codediv').html('');
				$('#solndiv').html('');
				return true;
			}
		},
		//dialogClass: 'no-close',
	});

	$('#loading-zone').dialog({
		width: document.body.clientWidth*0.8,
		height: document.body.clientHeight*0.7,
		modal: true,
		autoOpen: false,
	});
	$('#template-zone').dialog({
		width: document.body.clientWidth*0.8,
		height: document.body.clientHeight*0.7,
		modal: true,
		autoOpen: false,
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
	$('#listingQ').attr('onclick', "$('#loading-zone').dialog('open')");
	$('#loadA').attr('onclick', "$('#template-zone').dialog('open')");
	$('.template-row').attr('onclick', "selectRow($(this))");
	$('.cancel-template-load').attr('onclick', "clearTemplateLoad();");
	$('.load-template').attr('onclick','loadTemplate();');
	$("#previewform").nm();
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

	//create question object
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


	//attempt to preview the question
	questionPOST = {
		questiondata: questiondata
	};
	$.ajax('/assignment/assign/qpreview', {
		type: 'POST',
		async: false,
		data: questionPOST,
	}).done(function(response){
		alert(response);
		preview = jQuery.parseJSON(response)
	});
	if(preview.errors){ //tell them they have an error and quit
		alert(preview.errors);
		return;
	}

	//if a new question, add to the question list
	numQuestions = $('#questionsList').children().length;
	if(num > numQuestions){
		questionHTML = questionstring(num, $('#questiontitle').val());
		$('#questionsList').append(questionHTML);
	}

	//save the data to a hidden field
	datafield = $('#question'+num).find('input[type=hidden]');
	datafield.val(questiondata);

	//fill out the preview
	textPreview = $('#question'+num).find('.textPreview');
	textPreview.html(preview.text);
	solnsPreview = $('#question'+num).find('.solnsPreview');
	solnsPreview.html(preview.soln);

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
	var redo='';
	assignment = {
		title: '',
		start: '',
		due: '',
		questions: [],
	}
	//Test required forms
		assignment.title = $('#assigntitle').val();
		if(assignment.title == ''){
			redo+="Title\n";
		}
		else
			$('#assigntitle').style="";

		assignment.start = $('#assigndate').datepicker('getDate');
		if(assignment.start == null){
			redo+="Assign date\n";
		}
		else
			$('#assigndate').style="";

		assignment.due = $('#duedate').datepicker('getDate');
		if(assignment.due == null){
			redo+="Due date\n";
		}
		else
			$('#duedate').style="";

		if(redo!=''){
			var msg = "The following fields are required:\n"
			msg+=redo
			alert(msg);
			return false;
		}

	$('#questionsList>.question-whole').each(function(index){
		questiondata = $(this).find('input[type=hidden]').val();
		question = jQuery.parseJSON(questiondata);
		question.points = $(this).find('input[type=text]').val();
		console.log($(this).find('input[type=text]'))
		assignment.questions.push(question);
   });
	var overwrite;
	$.ajax('/assignment/utility/checktitle/', {
		type: 'POST',
		async: false,
		data: assignment,
	}).done(function(response){
		overwrite=jQuery.parseJSON(response);
	});

	if(overwrite.overwrite == true){
		if(confirm("Saving this will overwrite owned assignment of same name.\n Is this ok?")){
			$('#assignmentdata').val(JSON.stringify(assignment, undefined, 2));
   		$('#assignmentForm').submit();
   	}
   	else return;
	}

   $('#assignmentdata').val(JSON.stringify(assignment, undefined, 2));
   $('#assignmentForm').submit();
}

function previewQ(questiondata){
	//given questiondata, it will give you a preview
	// questiondata = $('#question'+num).find('input[type=hidden]').val();
	question = jQuery.parseJSON(questiondata);
	questionPOST = {
		questiondata: questiondata
	},

	$.ajax('/assignment/assign/qpreview', {
		type: 'POST',
		async: false,
		data: questionPOST,
	}).done(function(response){
		alert(response);
		return jQuery.parseJSON(response)
	});

}

function previewA(){
	//empty object
	assignment = {
		title: '',
		start: '',
		due: '',
		questions: [],		
	};

	assignment.title = $('#assigntitle').val();
	assignment.start = $('#assigndate').datepicker('getDate');
	assignment.due = $('#duedate').datepicker('getDate');

	$('#questionsList > .question-whole').each(function(index){
		questiondata = $(this).find('input[type=hidden]').val();
		question = jQuery.parseJSON(questiondata);
		question.points = $(this).find('input[type=text]').val();
		console.log($(this).find('input[type=text]'))
		assignment.questions.push(question);
   });

   $('#previewdata').val(JSON.stringify(assignment, undefined, 2));
   $('#previewform').submit();
}

function previewT(aid){
	previewHTML='<iframe class="iframe" src="assignment/assign/preview/'+aid+'"></iframe>';
	$(".template-area").append(previewHTML);
}

function iframe_preview(qid){
  previewHTML='<iframe src="assignment/question/'+qid+'" id="iframepreview'+qid+'"></iframe>';
  var ID="#";
  ID+=qid;
  $(ID).attr("class", "icon-eye-close");
  $(ID).attr("onclick", "iframe_close("+qid+")");
  $(".preview-area").append(previewHTML)
}
function iframe_close(qid){
  var ID = "#";
  ID+=qid;
  $("#iframepreview"+qid).remove();
  $(ID).attr("class", "icon-eye-open");
  $(ID).attr("onclick", "iframe_preview("+qid+")");
}
function loadExisting(){
	var ID='';
	var questionHTML='';
	//Close dialog box
	$( '#loading-zone' ).dialog('close');
	//Loop through selected elements
	$('.icon-eye-close').each(function(){
		ID='#';
		ID+=$(this).attr("id");
		//reset preview, eye
		$(ID).attr("class", "icon-eye-open");
  		$(ID).attr("onclick", "iframe_preview("+$(this).attr("id")+")")
  		$("#iframepreview"+$(this).attr("id")).remove();
		//append question data to list
		num = $('#questionsList').children().length+1;
		var data = $(ID+"data").attr("value");
		questionHTML=questionstring(num, $(ID+"title").attr("value"));
		$('#questionsList').append(questionHTML);
		$('#question'+num).find('input[type=hidden]').attr("value",data);
	});
}

function loadTemplate(){
	//Get assignment
	aid = $(".icon-ok").parent().parent().attr("id");
	//Clear current questions
	$('#questionsList>.question-whole').each(function(){
	   $(this).remove();
	});
	//Load in template details (title)
	$('#assigntitle').attr("value",$('#'+aid+'title').attr("value"));
	//Load in questions
	var data = jQuery.parseJSON($("#"+aid+"data").val()).questions;
	for(var qid in data){
		if(!data.hasOwnProperty(qid)) continue;
		num = $('#questionsList').children().length+1;
		var points = data[qid];
		var data = $('#'+qid+"data").attr("value");
		questionHTML=questionstring(num, $('#'+qid+"title").attr("value"));
		$('#questionsList').append(questionHTML);
		$('#question'+num).find('input[type=hidden]').attr("value",data);
		$('#question'+num).find('input[type=text]').attr("value",points);
	}
	//Delete evidence
	clearTemplateLoad();

}

function selectRow(element){
	$('.icon-ok').remove();
	$(element).children(".first-cell").append('<i class="icon-ok"></i>');
}

function clearTemplateLoad(){
	$(".iframe").remove();
	$('.icon-ok').remove();
	$( '#template-zone' ).dialog('close');
}

function questionstring(num, title){
	questionHTML=
		'<div id="question'+num+'" class="question-whole">\
			<div class="row-fluid questionMenu">\
				<input type="hidden"></input>\
			<div class="span5 question-description">'+
					title+
				'</div>\
				<div class="span1 btn question-edit" onclick="load_question('+num+')">\
					<i class="icon-edit-sign"> Edit</i>\
				</div>\
				<div class="span1 question-pts">\
					<input type="text" class="input-fit" value="0"></input>\
				</div>\
				<div class="span1 question-remove btn" onclick="remove_question('+num+')">\
					<i class="icon-remove-sign"></i>\
				</div>\
			</div>\
			<div class="row-fluid">\
				<div class="span10 offset1">\
					Question:\
					<div class="textPreview"></div>\
				<div>\
			</div>\
			<div class="row-fluid">\
				<div class="span10 offset1">\
					Solutions:\
					<div class="solnsPreview"></div>\
				</div>\
			</div>\
		</div>';
	return questionHTML;
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
