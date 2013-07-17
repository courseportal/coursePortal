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

code = CodeMirror.fromTextArea($('#code').get(0), CodeMirrorSettings);

$('#variable-zone').dialog({
	title: "VARIABLES",
	width: document.body.clientWidth*0.7,
	height: document.body.clientHeight*0.6,
	//modal: true,
	autoOpen: false,
	open: function(event, ui){
		var text = tinymce.activeEditor.getContent();
		var index = 0
		while(text.indexOf('$', index)>=0){
			index=text.indexOf('$', index)+1;
			var varName=findVar(text, index);
			if(varName==-1){
				alert("A Variable name is invalid!");
				return false;
			}
			//See if var is aready listed
			if($('#'+varName).length == 0){
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
							names[x]+"= <input type='text' name="+name+"_"+names[x]+"></input>";
						dataZone.append(inputString);
					}
				})
			}
			index+=1;
		}
	},
});

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

function validateAndSubmit(){
	$('#variable_list').children().each(function(){
		validate($(this));
		generate($(this));
	});
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

function validate(row){
	data={
		name:row.attr('id'),
		vartype: row.find('.variables').val(),
		input: '',
	};
	arr=[];
	row.find('.row-data').children().each(function(){
		arr.push($(this).val());
	});
	data.input = JSON.stringify(arr);
	$.ajax('/assignment/utility/validate/', {
		type: 'GET',
		async: false,
		data: data,
	}).done(function(response){
		if(response != 0){
			alert(data.name+" data is invalid:\n"+response);
			return false;
		}
	});
}

function generate(row){
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
	row.children('.row-data').children().each(function(){
		varName = $(this).attr('name').split('_')[1]; //Name of variable
		value = $(this).val(); //Value input
		genCode = varName+"="+value+"\n"+genCode;
	});
	code.setValue(genCode+"\n"+code.getValue());
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