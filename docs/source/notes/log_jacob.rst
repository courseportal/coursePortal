7/9/2013:
*Removed Nyromodal from the project, expanded use of jqueryUI
*Implemented use of google chart API to view boxplots of class performance
	**NOTE: boxplot is made by combining candlestick, line, and dot markers on a chart, google does not have a boxplot chart type
*Bugfixs

7/10/2013:
*Assignments can now be unassigned from students after being assigned.
*Assignments and questions can now be deleted without the use of an admin page.

7/11/2013:
*Separated due_date and start_date from assignment data field
	**NOTE: Data field now holds only a list of point values linked to question ids
*Fixed bugs in loading question templates, added back button
*Added owners field to questions
*Added ability to make questions/assignments private
	!NOT FULLY TESTED YET, EXPECT BUGFIXES IN THE FUTURE
*Slightly improved addQ HTML
*improved url system