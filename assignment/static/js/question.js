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

tinymce.init({
   selector: "textarea#problemText",
   force_p_newlines : false,
   width: document.body.clientWidth*.5
});

var CodeMirrorSettings = {
	mode: 'python',
	tabSize: 3,
	indentWithTabs: true,
	lineNumbers: true,
	theme: 'eclipse',
};

var validFlag = true;
var patt1=/\$[A-z]+[A-z0-9_]*/g;	
code = CodeMirror.fromTextArea($('#code').get(0), CodeMirrorSettings);

$(init);

function init(){
	$('#variable_list').sortable();

	$('#variable-zone').on('show', function() {
		var text = tinymce.activeEditor.getContent();
		var varNames=text.match(patt1);
		if(varNames!=null){
			for(var x=0; x<varNames.length; x++){
				addVar(varNames[x].substr(1));
			}
		
		}
	});

	$('#variable-zone').on('hidden',function(){
		$('#add_name').val('');
		$('#delete_name').val('');
	});

	initialInput($('#initialType').attr('value'), $('#initialAnswer').attr('value'), $('#initialChoice').attr('value'));
}


function addVar(varName){
	if(varName == '' || $('#'+varName).length != 0) return false;
	$('#variable_list').append(rowString(varName));
	var row = $('#'+varName).last();
	row.children('.typecell').html($('.variables').last().clone());
	variables=row.find('.variables');
	variables.attr('name', varName+"_"+variables.attr('name'));
	variables.change(function(){
		var name = $(this).val();
		if(name != "Custom"){
			data = {
				vartype : name,
			};
			$.ajax('/assignment/utility/matchType/', {
				type: 'GET',
				async: false,
				data: data,
			}).done(function(response){
				names=jQuery.parseJSON(response);
			});
			dataZone = $(this).parent().parent().children('.row-data').html('');
			name = $(this).parent().parent().attr('id');
			for(x=0; x<names.length; x++){
				inputString =
					names[x].name+"= <input type='text' style='width:100px' name="+name+"_"+names[x].name+" value="+names[x].defValue+"></input><br>";
				dataZone.append(inputString);
			}
		}
		else{
			$(this).parent().parent().children('.row-data').html('');
		}
	});
}


function rowString(varName){
	rowHTML = 
		"<tr id='"+varName+"'>\
			<td><i class='icon-remove' onclick='$(this).parent().parent().remove();'></i>"+varName+"</td>\
			<td class='typecell'></td>\
			<td class='row-data'></td>\
		</tr>";
	return rowHTML
}

function validateAndPreview(){
	pdata = {
		code:code.getValue(),
		text:tinymce.activeEditor.getContent(),
		choices:[],
		answer:$('#answer_input').children().first().val(),
	};
	if($('#tfTrue').prop('checked')){
		pdata.answer = true;
	}
	else if($('#tfFalse').prop('checked')){
		pdata.answer = false;
	}
	//Validate user input
	$('#variable_list').children().each(function(){
		validate($(this));
	});
	if(validFlag == false){
		validFlag = true;
		return false;
	}

	//Generate code
	tempCode = '';
	$('#variable_list').children().each(function(){
		tempCode = generate($(this), tempCode);
	});
	pdata.code = tempCode+"\n"+pdata.code;
	//Add choices
	$('#choice_input').children().each(function(){
		pdata.choices.push($(this).children().first().val());
	});
	pdata.choices = JSON.stringify(pdata.choices);
	
	//Eliminate $ in code
	pdata.code = pdata.code.replace(/\$/g,'');
	//test full code: looks for infinite loops and security errors
	var reply
	$.ajax('/assignment/utility/validateFull/', {
		type: 'GET',
		async: false,
		data: pdata,
	}).done(function(response){
		reply=response;
	});
	if(reply!=0){
		alert(reply);
		return false;
	}
	//Finally preview
	$('#preview-body').load('question/preview',pdata, function(response, status, xhr){
		MathJax.Hub.Queue(
      		["Typeset",MathJax.Hub,'preview-zone']
    	);
	});
	$('#preview-zone').modal('show');
}

function validateAndSubmit(){
	//Validate title and answer
	if($('#answer_input').children().first().val() == ''){
	   alert("Please give your question an answer");
	    return false;
    }
    if($('#question_title').val() == ''){
	    alert("Please give your question a title");
	    return false;
    }
    //Validate variable data input
	$('#variable_list').children().each(function(){
		validate($(this))
	});
	if(validFlag == false){
		validFlag = true;
		return false;
	}

	//Generate code
	var tempCode = '';
	$('#variable_list').children().each(function(){
		tempCode = generate($(this), tempCode);
	});
	tempCode = tempCode.concat("\n#CUSTOM\n",code.getValue());
	//test full code: look for infinite-loops and other run-time errors
	data={
		code:tempCode.replace(/\$/g,'')
	}
	var reply
	//Ajax call to test full code
	$.ajax('/assignment/utility/validateFull/', {
		type: 'GET',
		async: false,
		data: data,
	}).done(function(response){
		reply=response;
	});
	if(reply!=0){
		alert(reply);
		return false;
	}
	code.setValue(tempCode);
	code.toTextArea();
	$('#input_text').attr('value', tinymce.activeEditor.getContent());
	//Set choices
	choices=[];
	$('#choice_input').children().each(function(){
		if($(this).attr('class') == 'row-fluid'){
			choices.push($(this).children().first().val());
		}
		else{
			choices.push($(this).val());
		}
	});
	//Set atoms
	atoms=[]
	$('#atoms').children().each(function(){
		if($(this).prop("selected")){
			atoms.push($(this).attr('value'));
		}
	});
	$('#atom_list').attr('value', JSON.stringify(atoms));
	$('#choices').attr('value', JSON.stringify(choices));
    $.ajax('/assignment/question/create/',{
	    type: 'POST',
	    async: false,
	    data: $('#questionForm').serializeArray()
    });
    console.log($('#questionForm').serialize());
    window.location = '/assignment/';
}

function validate(row, dependent){
	var x=0;
	data={
		name:row.attr('id'),
		vartype: row.find('.variables').val(),
		input: '',
	};
	if(data.vartype == 'Custom'){
		return true
	}
	if(dependent == undefined)
		dependent = [];
	arr=[];
	row.find('.row-data').children("input").each(function(){
		if(validFlag == false){
			return false;
		}
		var varValue = $(this).val();
		//Check if this is defined by another variable
		if(varValue.match(patt1) != null){
			//Find dependencies
			currDependencies = varValue.match(patt1);
			//Check for any 'loops'
			if(dependent != undefined){
				for(var x=0; x<currDependencies.length; x++){
					for(var y=0; y<dependent.length; y++){
						if(currDependencies[x] == dependent[y]){
							validFlag = false;
							alert("Dependency loop detected in variables!");
							return false;
						}
					}
				}
			}
			//If no loop found
			//Add dependencies to list
			dependent.push(currDependencies);
			//recurse
			for(var x=0; x<currDependencies.length; x++){
				if(!validate($("#"+currDependencies[x].substr(1)), dependent)){
					return false;
				}
			}	
		}
		arr.push(varValue);
	});
	if(validFlag == false) return false;
	data.input = JSON.stringify(arr);
	$.ajax('/assignment/utility/validate/', {
		type: 'GET',
		async: false,
		data: data,
	}).done(function(response){
		if(response != 0){
			alert("\""+data.name+"\" data is invalid:\n"+response);
			x=response;
		}
	});
	if(x != 0){
		validFlag=false;
		return false;
	}
	return true;
}

function generate(row, tempCode){
	data={
		vartype: row.find('.variables').val(),
	};
	if(data.vartype == 'Custom'){
		return tempCode;
	}
	$.ajax('assignment/utility/getTypeCode', {
		type: 'GET',
		async: false,
		data: data,
	}).done(function(response){
		genCode = response;
	});
	//Format code to generate
	genCode=genCode.replace('__this', row.attr('id'));
	genCode=jQuery.parseJSON(genCode);
	genCode="#Template Code\n"+genCode;
	row.children('.row-data').children("input").each(function(){
		varName = $(this).attr('name').split('_')[1]; //Name of variable
		value = $(this).val(); //Value input
		genCode = varName+"="+value+"\n"+genCode;
	});
	tempCode = tempCode.concat('\n#var:',data.vartype,'_',row.attr('id'),'\n',genCode);
	return tempCode;
}

function inputChange(questionType){
	$('#choice_input').html('');
	if(questionType == "True/False"){
		html=
			"<input type='radio' name='answer' id='tfTrue' value='True' checked>True</input>\
			<input type='radio' name='answer' id='tfFalse' value='False'>False</input>";
		$('#answer_input').html(html);
	}else if(questionType == "Short Answer"){
		html=
			"<input type='text' name='answer' placeholder='answer'></input>";
		$('#answer_input').html(html);
	}else if(questionType == "Multiple Choice"){
		html=
			"<input type='text' name='answer' placeholder='answer'></input>";
		$('#answer_input').html(html);
		html=
			"<div class='row-fluid'>\
				<input type='text' placeholder='choice'></input>\
				<div class='btn' onclick='addChoice()'>Add Choice</div>\
			</div>";
		$('#choice_input').html(html);
	}
}

function initialInput(type, solution, choices){
	inputChange(type);
	if(type != 'True/False'){
		$('#answer_input').children('[name="answer"]').attr('value', solution);
	}
	else if(solution == 'True'){
		$('#tfTrue').prop('checked', true);
	}
	else{
		$('#tfFalse').prop('checked', true);
	}
	if(type == 'Multiple Choice'){
		choices=jQuery.parseJSON(choices);
		for(var x=0; x<choices.length; x++){
			$('#choice_input').find('input').last().attr('value', choices[x]);
			if(x != choices.length-1){
				addChoice();
			}
		}
	}
}

function addChoice(){
	html=
		"<div><input type='text' placeholder='choice'></input><i class='icon-remove' onclick='$(this).parent().remove()'></i></div>";
	$('#choice_input').append(html);
}

$(document).ajaxError(function(event, request, settings) {
  alert( "Error requesting page " + request.responseText);
});