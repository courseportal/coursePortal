
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

	$('.icon-eye-open').popover({trigger:'manual', placement:'left'});
	//Element attributes set
	$( '#opener' ).attr('onclick', "load_question($('#questionsList').children().length+1)");
}

function load_question(num){ 
	$('#questionNum').val(num);
	$( '#dialog-body' ).load('question/'+num);
	MathJax.Hub.Queue(
      	["Typeset",MathJax.Hub,'dialog-body']
    );
	$( '#dialog' ).modal('show');
}

function remove_question(num){
	if(confirm('Are you sure you want to remove this question?'))
		$('#question'+num).remove();
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

		assignment.start = $('#assigndate').val();
		if(assignment.start == null){
			redo+="Assign date\n";
		}
		else
			$('#assigndate').style="";

		assignment.due = $('#duedate').val();
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

	$('#assignmentdata').val(JSON.stringify(assignment, undefined, 2));
	$.ajax('/assignment/create/',{
		type:'POST',
		async:false,
		data:$('#assignmentForm').serialize()
	});
	//$('#assignmentForm').submit();
	window.location = '/assignment/'
}

function previewA(){
	//empty object
	assignment = {
		title: '',
		questions: [],		
	};

	assignment.title = $('#assigntitle').val();

	$('#questionsList > .question-whole').each(function(index){
		questiondata = $(this).find('input[type=hidden]').val();
		question = jQuery.parseJSON(questiondata);
		assignment.questions.push(question);
    });

    data = {
   	    previewdata:JSON.stringify(assignment, undefined, 2),
    };

    $('#preview-body').load('preview/', data, function(response, status, xhr){
   		if (status == "error") {
    		var msg = "Sorry but there was an error: ";
    		$("#preview-body").html(msg + xhr.status + " " + xhr.statusText);
  		}
  		else{
  			MathJax.Hub.Queue(
      			["Typeset",MathJax.Hub,'previewModal']
    		);
  		}
    });
    $('#previewModal').modal('show');
}

function iframe_preview(qid){
  previewHTML='<iframe src="assignment/question/'+qid+'" id="iframepreview'+qid+'"></iframe>';
  var ID="#";
  ID+=qid;
  $(ID).children('.icon-eye-open').data('popover').tip().find('.popover-content').empty().append(previewHTML);
  $(ID).children('.icon-eye-open').popover('show');
  $(ID).children('.icon-eye-open').attr("onclick", "iframe_close("+qid+")");
  $(ID).children('.icon-eye-open').attr("class", "icon-eye-close");
  //$(".preview-area").append(previewHTML);
}

function iframe_close(qid){
  var ID = "#";
  ID+=qid;
  //$("#iframepreview"+qid).remove();
  $(ID).children('.icon-eye-close').popover('hide');
  $(ID).children('.icon-eye-close').attr("onclick", "iframe_preview("+qid+")");
  $(ID).children('.icon-eye-close').attr("class", "icon-eye-open");
}

function loadExisting(){
	var ID='';
	var questionHTML='';
	//Close modal box
	$('#loading-modal').modal('hide')
	//Close any open previews
	$('.icon-eye-close').each(function(){
		iframe_close($(this).parent().attr("id"));
	});	
	//Loop through selected elements
	$('.load-selector:checked').each(function(){
		$(this).removeProp('checked');
		ID='#';
		ID+=$(this).parent().attr("id");
		//append question data to list
		num = $('#questionsList').children().length+1;
		questionHTML=questionstring(num, $(ID+"title").attr("value"), $(this).parent().attr('id'));
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
					<button class="span1 question-remove btn" onclick="remove_question('+num+')">\
						<i class="icon-remove-sign"></i>\
					</button>\
				</div>\
			</div>';
	return questionHTML;
}

$(document).ajaxError(function(event, request, settings) {
  alert( "Error requesting page " + request.responseText);
});
