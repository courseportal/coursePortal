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

7/29/2013:
Spent mostly planning the week, however small improvements were made:
	*Choices now randomize order for multiple choice questions
	{*Assign date now determines when studetns can view an instance
	{*Due date determines when assignments can no longer be edited
	{Testing the above two features over the course of this week
*Bugfixes to assigning
!BUG: edit an assignment yet do not change start/due date -> dates revert to now.

7/30/2013:
*Initial test of due date system is succesful, no bugs detected
*Fixed bugs in previewing assignments written by others
*Questions can be searched and sorted by related atoms when making an assignment
*Questions now have a difficulty rating determined by how often students get it correct
	*questions can be searched by difficulty when adding them to assignments
*various small bugfixes

7/31/2013:
*small bugfixes
*Added the ability for students to do practice questions related to some atom

8/1/2013:
*Questions create a copy when they are made, consequences of this:
	*If someone changes original question, question does not change in your assignment
	*Copy questions cannot be edited or deleted
	*Copy questions are shared between multiple people
	*If a copy question has no owners and the original question is changed, copy question is deleted
*Similarly, loading an assignment now creates a copy which can be deleted whenever. However:
	*Questions in copies cannot be edited
	*Dates and point values can be edited
	*Title cannot be changed

8/2/2013:
*fixed bugs in the question creation process
*When loading assignments, assignments can now be sorted and searched by Title and Author
	*Sorting by subject in the working
*Atoms can be searched and sorted by name and number of related questions when doing practice
*fixed bugs in student practicing

8/5/2013:
*Mathjax now processes text every time you preview a question rather than just the first time
*Questions can be reported as broken from the practice area
	*Emails creator user-submitted text. 
*Subjects for each question sorted alphabetically

8/6/2013:
*Assignments can now contain multiple copies of the same question with different point values.
*Fixed bugs in previewing assignments
*Due Dates can be extended
*improved variable system in adding questions
*Practice html improved

8/7/2013:
I have decided not to implement a viewing field in the variable type model, because generated code section declares how the variable will display in text, it is simpler to just allow the user to declare said representation as an html string when creating the variable type.
*Variable data fields can have default values specified
*Variable type can be specified in variable list area and will be tested automatically
	*It is no longer necessary to test for the correct data type in validation code or cast it to be such.
	*TODO: create testing for a default type
Variables should now be specified in the following format:
name,type,default
	name: The name of the variable
	type: What type data provided should be. This will be automatically tested.
	default: A default value for the variable.
*Removed jqueryUI from addQ.html
*Removed jqueryUI from addassignment.html

8/8/2013:
*System will test memory usage and runtime of submitted code, this feature will only work if the website is run in a unix environment
*Questions can be edited after being created
	TODO: test that edited question behaviour is as desired

8/9/2013:
*Editing questions now fully implemented
*Bugfixes
*User can now create two assignments of same name without overwriting one or the other
*Edit assignment will overwrite old assignment with same id rather than create new assignment

8/12/2013:
*Fixed bugs in the deletion of questions
*Fixed bugs in creation of assignments
*Assignments and questions can now be picked from a searchable/sortable table to edit
