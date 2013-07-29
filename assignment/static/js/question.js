//'/[^/]$/g'

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

var fullTestFlag = false;
var validFlag = true;
var patt1=/\$[a-zA-Z][a-zA-Z0-9_]*/g;

code = CodeMirror.fromTextArea($('#code').get(0), CodeMirrorSettings);
$('#variable_list').sortable();

$('#variable-zone').dialog({
	title: "VARIABLES",
	width: document.body.clientWidth*0.7,
	height: document.body.clientHeight*0.6,
	modal: true,
	autoOpen: false,
	open: function(event, ui){
		var text = tinymce.activeEditor.getContent();
		var index = 0
		while(text.indexOf('$', index)>=0){
			index=text.indexOf('$', index)+1;
			var varName=findVar(text, index);
			if(varName==-1){
				continue;
			}
			//See if var is aready listed
			addVar(varName);
			index+=1;
		}
	},
	close: function(event, ui){
		$('#add_name').val('');
		$('#delete_name').val('');
	},
});

$('#preview-zone').dialog({
	title: "PREVIEW",
	width: document.body.clientWidth*0.7,
	height: document.body.clientHeight*0.6,
	modal:true,
	autoOpen:false,
});

function addVar(varName){
	if(varName == '' || $('#'+varName).length != 0) return false;
	$('#variable_list').append(rowString(varName));
	var row = $('#'+varName).last();
	row.children('.typecell').html($('.variables').last().clone());
	variables=row.find('.variables');
	variables.attr('name', varName+"_"+variables.attr('name'));
	variables.change(function(){
		var name = $(this).val();
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
				names[x]+"= <input type='text' name="+name+"_"+names[x]+"></input><br>";
			dataZone.append(inputString);
		}
	});
}

function delVar(varName){
	$('#'+varName).remove();
}

function rowString(varName){
	rowHTML = 
		"<tr id='"+varName+"'>\
			<td>"+varName+"</td>\
			<td class='typecell'></td>\
			<td class='row-data'></td>\
		</tr>";
	return rowHTML
}

function viewVariables(){
	$('#variable-zone').dialog('open');
}

function findVar(str, index){
	//Make these global strings later
	characters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
	full=characters+'1234567890_';
	varName='';
	//Check first value is fine
	if(characters.indexOf(str[index]) == -1){
		return -1;
	}
	//Run while characters are fine
	while(full.indexOf(str[index]) >= 0){
		varName+=str[index];
		index+=1;
	}
	return varName;
}

function validateAndPreview(){
	pdata = {
		code:code.getValue(),
		text:tinymce.activeEditor.getContent(),
		choices:[],
		answer:$('#answer_input').children().first().val(),
	};
	$('#variable_list').children().each(function(){
		validate($(this));
		
	});
	if(validFlag == false){
		validFlag = true;
		return false;
	} 
	tempCode = '';
	$('#variable_list').children().each(function(){
		tempCode = generate($(this), tempCode);
	});
	pdata.code = tempCode+"\n"+pdata.code;
	//Add choices
	$('#choice_input').children().each(function(){
		if($(this).attr('class') == 'row-fluid'){
			pdata.choices.push($(this).children().first().val());
		}
		else{
			pdata.choices.push($(this).val());
		}
	});
	pdata.choices = JSON.stringify(pdata.choices);
	//test full code if necessary
	var reply
	if(fullTestFlag){
		fullTestFlag=false;
		///Eliminate $
		pdata.code = pdata.code.replace(/\$/g,'');
		//Ajax call to test full code
		$.ajax('/assignment/utility/validateFull/', {
			type: 'GET',
			async: false,
			data: pdata,
		}).done(function(response){
			fullTestFlag = false;
			reply=response;
		});
		if(reply!=0){
			alert(reply);
			return false;
		}
	}
	$('#preview-zone').load('question/preview',pdata, function(response, status, xhr){
		$('#preview-zone').dialog('open');
	});
}

function validateAndSubmit(){
	$('#variable_list').children().each(function(){
		validate($(this))
	});
	if(validFlag == false){
		validFlag = true;
		return false;
	} 
	tempCode = '';
	$('#variable_list').children().each(function(){
		tempCode = generate($(this), tempCode);
	});
	tempCode += "\n"+code.getValue();
	//test full code if necessary
	if(fullTestFlag){
		data={
			code:tempCode.replace(/\$/g,'')
		}
		var reply
		fullTestFlag=false;
		//Ajax call to test full code
		$.ajax('/assignment/utility/validateFull/', {
			type: 'GET',
			async: false,
			data: data,
		}).done(function(response){
			fullTestFlag = false;
			reply=response;
		});
		if(reply!=0){
			alert(reply);
			return false;
		}
	}
	code.setValue(tempCode);
	$('#input_text').attr('value', tinymce.activeEditor.getContent());
	choices=[];
	$('#choice_input').children().each(function(){
		if($(this).attr('class') == 'row-fluid'){
			choices.push($(this).children().first().val());
		}
		else{
			choices.push($(this).val());
		}
	});
	$('#choices').attr('value', JSON.stringify(choices));
	$('#questionForm').submit();
}

function validate(row, dependent){
	var x=0;
	data={
		name:row.attr('id'),
		vartype: row.find('.variables').val(),
		input: '',
	};
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
			if(!fullTestFlag) fullTestFlag=true;
			//Find dependencies
			currDependencies = varValue.match(patt1);
			//Check for any 'loops'
			if(dependent != undefined){
				for(var x=0; x<currDependencies.length; x++){
					for(var y=0; y<dependent.length; y++){
						if(currDependencies[x] == dependent[y]){
							fullTestFlag = false;
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
			fullTestFlag = false;
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
	row.children('.row-data').children("input").each(function(){
		varName = $(this).attr('name').split('_')[1]; //Name of variable
		value = $(this).val(); //Value input
		genCode = varName+"="+value+"\n"+genCode;
	});
	tempCode = tempCode+'\n'+genCode;
	return tempCode;
}


function inputChange(questionType){
	$('#choice_input').html('');
	if(questionType == "True/False"){
		html=
			"<input type='radio' name='answer' value=1>True</input>\
			<input type='radio' name='answer' value=0>False</input>";
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

function addChoice(){
	html=
		"<input type='text' placeholder='choice'></input>";
	$('#choice_input').append(html);
}

$(document).ajaxError(function(event, request, settings) {
  alert( "Error requesting page " + request.responseText);
});