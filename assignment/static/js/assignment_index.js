$(init); //runs init after DOM is loaded
function init(){
	$('.assignment-row').attr('onclick', "selectRow($(this))");
	$('.load-assignment').attr('onclick', "loadAssignment()")
}

function previewL(aid){
	previewHTML='<iframe class="iframe" src="assignment/preview/'+aid+'"></iframe>';
	$(".assignment-area").html(previewHTML);
}

function selectRow(element){
	$('.icon-ok').remove();
	$(element).children(".first-cell").append('<i class="icon-ok"></i>');
}

function loadAssignment(){
	var aid = $('.icon-ok').parent().attr("id");
	if(aid == undefined){
		alert("No assignment selected to load");
		return false;
	}
	window.location = "edit/"+aid;
}