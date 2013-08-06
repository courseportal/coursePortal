
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
	tabSize: 2,
	lineNumbers: true,
	indentWithTabs: true,
	theme: 'solarized-light'
};

code = {};
solution = {};
choices = [];

$(init); //runs init after DOM is loaded
function init(){
	//create sortable
	$( '#questionsList' ).sortable({
		update: function(event, ui) {
	      $('#questionsList>.row-fluid').each(function(index){
	      	num = index+1;
	      	$(this).attr('id', 'question'+num)
	        $(this).find('.question-remove').attr('onclick', 'remove_question('+num+')');
	      });
	   },
	});

	//init the dialog
	$( '#dialog' ).dialog({ 
		width: document.body.clientWidth*0.8,
		height: document.body.clientHeight*0.5,
		modal: true,
		distance: 10,
		overflow: scroll,
		autoOpen: false,
		draggable: false,
		resizable: false,
		focus: function(event, ui){
			//disable parent scrolling
			$('body').addClass('dialog-open');
		},
		close: function(event, ui){
			//re-enable parent scrolling
			$('body').removeClass('dialog-open');
		},
	});

	$('#loading-zone').dialog({
		width: document.body.clientWidth*0.8,
		height: document.body.clientHeight*0.7,
		modal: true,
		autoOpen: false,
	});

	$('#previewform').dialog({
		width: document.body.clientWidth*0.8,
		height: document.body.clientHeight*0.7,
		modal: true,
		autoOpen: false,
		focus: function(event, ui){
			//disable parent scrolling
			$('body').addClass('dialog-open');
		},
		close: function(event, ui){
			//re-enable parent scrolling
			$('body').removeClass('dialog-open');
		}
	});
	//init wysiwyg
	tinymce.init({
	   selector: 'textarea#text',
	   force_p_newlines : false 
	});
	//init dialogPreview height
	 	

	//initalize datepickers
	$('#assigndate').datepicker({ dateFormat: "yy-mm-dd" });
	$('#duedate').datepicker({ dateFormat: "yy-mm-dd" });
	//Element attributes set
	$( '#opener' ).attr('onclick', "load_question($('#questionsList').children().length+1)");
	$('#listingQ').attr('onclick', "$('#loading-zone').dialog('open')");
}

function load_question(num){ 
	$('#questionNum').val(num);
	//change save destination
	$( '#dialog' ).load('question/'+num);
	$( '#dialog' ).dialog('open');
	//open the dialog
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
		question = {
			id: 0,
			points: 0,
		}
		question.id = $(this).find('input[type=hidden]').val();
		question.points = $(this).find('input[type=text]').val();
		assignment.questions.push(question);
    });
	//Check if already own assignment by same name
	var overwrite;
	$.ajax('/assignment/utility/checktitle/', {
		type: 'POST',
		async: false,
		data: assignment,
	}).done(function(response){
		overwrite=jQuery.parseJSON(response);
	});

	if(overwrite.overwrite == true)
		if(!confirm("Saving this will overwrite owned assignment of same name.\n Is this ok?"))
			return;
	$('#assignmentdata').val(JSON.stringify(assignment, undefined, 2));
	$('#assignmentForm').submit();
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
		assignment.questions.push(question);
    });

    data = {
   	    previewdata:JSON.stringify(assignment, undefined, 2),
    };

    $('#previewform').load('preview/', data, function(response, status, xhr){
   	if (status == "error") {
    		var msg = "Sorry but there was an error: ";
    		$("#previewform").html(msg + xhr.status + " " + xhr.statusText);
  		}
    });
    MathJax.Hub.Queue(
      	["Typeset",MathJax.Hub,'previewform']
    );
    $('#previewform').dialog('open');
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
		questionHTML=questionstring(num, $(ID+"title").attr("value"), $(this).attr('id'));
		$('#questionsList').append(questionHTML);
	});
}

function questionstring(num, title, id){
	questionHTML = 
		'<div class="question-whole" id="question'+num+'">\
				<div class="row-fluid questionMenu">\
					<input type="hidden" value="'+id+'"></input>\
				<div class="span5 question-description">'+
						title+
					'</div>\
					<div class="span1 btn question-edit" onclick="load_question('+id+')">\
						<i class="icon-eye-open"> View</i>\
					</div>\
					<div class="span1 question-pts">\
						<input type="text" class="input-fit" value="0"></input>\
					</div>\
					<div class="span1 question-remove btn" onclick="remove_question('+num+')">\
						<i class="icon-remove-sign"></i>\
					</div>\
				</div>\
			</div>';
	return questionHTML;
}
