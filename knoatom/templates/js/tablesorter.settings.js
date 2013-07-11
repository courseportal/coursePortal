{% comment %}/*
This is a templated javascript file
Include this file surrounded by <script></script> tags.  Set the variables you want, otherwise
the defaults will be used.  The table you want to use tablesorter on must only have the class
'tablesorter'.  The rest of the classes will be set by including with "classes='classA classB'".
e.g.
<script>{% include 'js/tablesorter.settings.js' with table='#myTable' classes='table' sortList='[[0,0]]' %}</script>

For the settings sortList, sortAppend and sortForce the list that you provide is a list of lists.  The order matters.  eg [[0,0]].  Each sublist has 2 elements.  The first is which row you want to sort by starting at 0.  The second is whether you want to sort ascending (0) or descending (1).

Django Variables:
	
	table		The identifier for the table, eg '#myTable' or 'table.tablesorter'.  The default is
				'table' which will affect all tables in the html file.  Default: 'table'

	classes		The classes that you want the table to have. Default: 'table table-bordered'

	sortList	The order you want the table to be sorted by initially.  Default: []

	sortAppend	The sorting that you want to append all user sorts by.  Default: []

	sortForce	The sorting that you want to prepend to all user sorts.  Default: []

*/

// tablesorter 2.10.8
// Documentation found here:
// http://mottie.github.io/tablesorter/docs/index.html

// Bootstrap specific example here:
// http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
{% endcomment %}
$(function() {

  $.extend($.tablesorter.themes.bootstrap, {
	// these classes are added to the table. To see other table classes available,
	// look here: http://twitter.github.com/bootstrap/base-css.html#tables
	table		: {{ classes|default:'table table-bordered' }},
	header		: 'bootstrap-header', // give the header a gradient background
	footerRow	: '',
	footerCells	: '',
	icons		: '', // add "icon-white" to make them white; this icon class is added to the <i> in the header
	sortNone	: 'bootstrap-icon-unsorted',
	sortAsc		: 'icon-chevron-up',
	sortDesc	: 'icon-chevron-down',
	active		: '', // applied when column is sorted
	hover		: '', // use custom css here - bootstrap class may not override it
	filterRow	: '', // filter row class
	even		: '', // odd row zebra striping
	odd			: ''  // even row zebra striping
  });

  // call the tablesorter plugin and apply the uitheme widget
  $("{{ table|default:'table' }}").tablesorter({
	// this will apply the bootstrap theme if "uitheme" widget is included
	// the widgetOptions.uitheme is no longer required to be set
	theme : "bootstrap",

	widthFixed: true,

	headerTemplate : '{content} {icon}', // new in v2.7. Needed to add the bootstrap icon!
	// Set to sort initially by votes in descending order and name in ascending order
	sortList : {{ sortList|default:'[]' }},
	sortForce : {{ sortForce|default:'[]' }},
	sortAppend : {{ sortAppend|default:'[]'}},
	
	// Set to always append a sort by votes in descending order on all user sorting
	
	
	

	// widget code contained in the jquery.tablesorter.widgets.js file
	// use the zebra stripe widget if you plan on hiding any rows (filter widget)
	widgets : ["uitheme"] //,, "filter", "zebra" ],

   
  })

});