TODO list:
+ Change how questions are made
+ Loaded assignments/questions can't be edited
+ Metrics look at assignments, not classes


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
	EDIT:DELETED
*Slightly improved addQ HTML
*improved url system

7/12/2013:
*Templates can now be deleted
*More in-depth testing and bugfixing performed

7/15/2013:
After discussion with professor, following features have been REMOVED:
	1.Ability to make things 'private'; everything will be public in some fashion
	*question and assignment model field 'private' removed
	2.Current template system. Functionality will be folded into the question system somehow. In the future, templates will be a way of styling a question.
	*Models 'template' and 'Atemplate' removed, andd corresponding views/templates
*Classes relate to assignments, questions relate to atoms

week of 7/26:
Past two weeks have been spent creating a new model called a 'variable type'. This essentially allows users to use pre-written code chunks to create a question. Variable types have the following fields:
	VARIABLES: a list of the data that user must provide for the code chunk to work
	VALIDATION CODE: Optional, code that can be run to validate data provided by the user. Sets a variable called "result" to some helpful error message if the data is not good.
	GENERATED CODE: This is thee code that will be generated in the question's code section, with '__this' being replaced by the specified variable name. Assignments for necessary data will be pasted in beforehand.
This has been tested with question/assignment creation, deletion, and instantiation and currently works. Additionally, variable data can be defined by other variables. Currently, I am working on expanding the type moel with the following features:
	*Allow the variables list to declare variable types, which can then be automatically tested instead of requiring validation code to include said tests.
	*Allow variable list to declare default values.
	*Include a 'viewing html' field, which determines the way that the variable displays on a page.
Additionally, the following types should be created:
	*Set
	*graph
	*Equation (?Maybe not, mathjax does provide inline math fonts that are fairly easy to use?)
	*graph theory graph

		

