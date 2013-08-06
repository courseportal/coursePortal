$.fn.dataTableExt.ofnSearch['html'] = function ( sData ) {
    var n = document.createElement('div');
    n.innerHTML = sData;
    if ( n.textContent ) {
        return n.textContent.replace(/\n/g," ");
    } else {
        return n.innerText.replace(/\n/g," ");
    }
}