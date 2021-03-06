.. _log_nick:

======================
Nick's Development Log
======================

.. contents:: Table of Contents
	:local:

This is where I will keep a log of what I'm working on, problems I'm having, or just notes in general.

Goals
-----

Goals for 2 weeks when I am gone:
	*	Finish fixing what I have broken:
		
		*	'post'
		*	voting
	
	*	Refactor code
	*	Document code
	*	Test code
	*	Deploy to test server
	
		*	How important is the existing data?
		
	*	MathJax in formus

Different scores for different atoms
Multiple tags for everything [x]
questions are related to atoms like tags? weighted list?
questions/assignments not related to classes, except professors can assign assignments. But everyone can still see them.
	
Todo:
	*	Work with the url system
	*	Fix the 'post' view or remove it and reimplement functionality
	*	Do we want multiple videos?
	*	Refactor account, put validation in forms
	*   Implement ajax table updating in the topic list
	*   Testing
	*   Documentation
	*	Refactor
	*	More validation for uploaded file types
	*	Integrate forum into Atom better
	
Week of July 15-19
==================

*	Finished refactoring ``home.py``.  Cut the length from 700+ lines to 150 lines and 100 lines of helper functions in a seperate file
*	While refactoring ``home.py`` I also started to refactor the templates that it utilizes.
*	Changed user uploaded content from a ForeignKey to atoms to a ManyToMany.
*	Removed the video ``post`` view.
*	Updated ``web/models.py`` to be more consistent.

Week of July 8-12
=================

*	Finished class edit form

	*	It uses AJAX to submit all data, but still works without AJAX.  However you cannot edit categories without javascript, but you can make new ones.
	*	On this page you can edit the class as well as create and edit categories
	*	There is a 'finder-like' view of the categories in the class that you can double click on a category to edit it.
	*	The buttons and titles change based on wether you are editing or creating a new category.
	*	The 'finder-like' columnview of the categories refreshes when you create/update a category.
	*	The columnview uses AJAX to get one level of the hierarchy at a time for faster loading. 
	*	Added delete category button when we are editing a category
	
*	Added a delete button to all of the user uploaded submission pages when you are updating.
*	Put the class summary in the class "home" page.  HTML markup is allowed.
*	Created a universal breadcrumb generating function to replace old version
*	Moved the report form to its own view and removed the need for a context variable for an empty ReportForm by using a template tag.
	
Week of July 1-5
================

*	Finished class creation form
*	Started work on class edit form

	*	Added support for creating/editing multiple categories at a time in the class edit form using formsets
	*	Removed support for creating/editng multiple categories at a time because it is simpler to program and use a form that only allows creating one category at a time.
	*	Added support for creating categories one at a time in the class edit form

Week of June 24-28
==================

*   Moved all functionality related to bug reports from ``web/`` to ``knoatom/``.
*   Added a custom templatetag in ``knoatom/templatetags/`` to import the bug report form and abstract that functionality out of the views
*   Now the bug report should work for every view that extends ``base.html`` automatically
*   Moved the rating system into a seperate app
*   Added rating for topics in forum
*   Forum now orders topics by votes
*   Creating new view for creating classes

Week of June 17-21
==================

So far this week I have:
	*   Added custom validation to the exposition form to ensure that the link begins with ``http://`` or ``https://``
	*   Changed the video display list to a sortable table to be consistent with the rest of the content display lists
	*   Added a sticky feature for content lists in classes
		
		*   First I added a sticky field for each content type in the Class model
		*   Then I added functionality to force the table sort to be prepended by a sort on sticky/not stickied by adding a hidden column for sticky status
		*   Then I added a button for ``authors`` and ``allowed_users`` of a class to be able to sticky content in the content list for videos, expositions, notes and examples.
		
			*   I used AJAX to have the (not) stickied change be reflected in the table without reloading the page
			*   Then I added automatic table updating and resorting when the votes or sticky status is changed
		
		*   When users are creating new content there is a new field ``classes_to_sticky_in``
			
			*   If the user isn't the ``author`` or an ``allowed_user`` of any class then the field is hidden
			*   Otherwise it shows all the classes that they are the ``author`` of or an ``allowed_user`` in and allows them to select the classes they wish the submission to be stickied in
			
	*   Abstracted the modal for reporting content to another template because it was repeated 8 times.
	*   Changed the deletion of content from linking users to a new page and instead use AJAX and a modal
	
		*   When a user tries to delete an object a confirmation modal pops up
		*   If they click yes an AJAX script fires that calls the view and deletes the object and it returns the required variables
		*   Then the function deletes the row from the table that the content was in and updates the table data
		
	*   Changed some minor aesthetic stuff in the content list templates so that weird underlines don't show up when hovering over the icons
	*   Added tooltips to the option icons
	*   Changed the vote system so that the values are abstracted into one place so that it is easy to change in the future
	*   Added some code to my delete content AJAX function to update the user rating when you delete the object so it is reflected on the screen without refreshing.

Week of June 9-14
==================

So far this week so far I have:
	*   Fixed the forum poll system
	*   Added the ability for all users to submit new content for:

		-   Expositions
		-   Lecture Notes
		-   Examples
		
		Lecture Notes and Examples are limited to ``.pdf`` files right now.  The ``ALLOWED_FILE_EXTENSIONS`` setting in ``settings.py`` sets the allowed file extensions.  We should probably do more type checking than just this because people can lie.
		
	*   I have been adding documentation as I go to various functions and classes.
	*   Added the ability for the owner of a user submitted object and all staff/superusers to edit/delete that object where they are listed.  This works for:
		
		-   Expositions
		-   Lecture Notes
		-   Examples
		-   Videos
	
	*   Improved aesthetics of exposition/note/example display list
	*   Added sorting features to exposition/notes/example display list
		
		*   Default sort is by the votes and users can sort by whatever they want to
		
	*   Changed the class list to use the same sortable table that user uploaded content is displayed in
	*   Changed the class list so only active classes show up to everyone.  Inactive classes show up to:
	
		*   The superuser
		*   The class author
		*   The allowed users of the class
			
	*   If a user tries to access the class by typing in the URL and they don't have access then they will be redirected to the ``'class_index'`` page.

Week of June 3-7
================

This week I implemented the forums and completly changed the template structure.

I used the `Pybbm forums<https://pybbm.readthedocs.org/en/latest/index.html>`_ to implement the forums.  Most of it was fairly easy to integrate as it was built to be able to easily plug into an existing project.  I had a few problems though including:
	*	The template took some time to set up so that it works
	*	I had some problems with urls.py because of the ordering and the regexs used
	*	The poll feature wasn't working and it took me forever to find out why, now it is half working and I have a good idea on how to fix the other part

Then I once I got the forums (almost) working I started to work on integrating it into the site.  First I implemented the admin part so that when you create/edit/delete an atom the cooresponding forum gets created/edited/deleted.  Then I started working on changing the templates so that I can integrate the forums into the site.  When I was changing the templates I realized that our current templates were very messy in that:
	*	``base.html`` was very janky and had a lot of content in it where it really should only be a theme/style for the rest of the site with very little content, all of which should be overridable.
	*	There was a lot of duplicate code throughout the whole template system making it very hard to make chages because you had to make changes in 5 places
	*	We used the same template for the class, category, atom and post views so they were very cluttered and had a lot of ``{% if variable_exists %}`` statements when you should really be using blocks and extending templates.
	*	Some of it was just plain wrong and some of it was unneeded
	
I went through and completly changed the template system and documented it.  You can see the documentation and a guide on how the templates should be set up :ref:`here<templates>`.

Lastly I worked on implementing the forum into the atom view as well as creating a link to the base forum. 

Week of May 27-31
=================

This week I mainly worked on overhauling the atom orginazational system:
	*	First I seperated Categories from Atoms.
		
		*	Atoms contain all of the information
		*	Categories only provide the structure
		
	*	I then changed the way the Navigation bar was displayed on screen.  Initially it could only display "2 levels" of hierarchy.  Now it recurses in the template from the top of the Category tree to all of the "top level categories" children.
		
		.. note::
		
			This introduced a problem where infinite recursion could happen if there are loops in the Category system which Taoran has solved in the admin page.
		
	*	Then I added a Base_Category Foreign Key to Atom so that every atom must be attributed with a default category which we use to display the Atoms outside of the class view.
	*	I changed the home page from a class list view to a view of the base categories and the videos in the atoms, much like the class view exept that all atoms are shown, not just the ones in that particular class.
	*	I changed the class list view to its own URL and added a link to it in the Navigation Bar.
	*	I changed the "Submit New Content" feature from being class instanced to being outside the class view and it submits content site-wide:
	
		*	Changed the URL from /class/submit, /class/post, ... to /submit, /post, ...
		*	Changed everything that links to it because the URL takes 1 less argument now
		
	*	Then I tried to remove everything that I can from base.html so it can be used site wide because having more than one copy of base.html that we use in different places that is slightly modified is a pain and hard to keep updated.
	
Then I started working on documentation:
	*	I downloaded sphinx and started figuring out how the automatic documentation process works.
	*	I wrote an extremely detailed installation guide for mac so that future people added to the project have a good guide for installation
	*	I set up the documentation structure for the project so that all docstrings are automatically added to the documentation.
	*	I set up gh-pages and made an auto-update script to have our documentation hosted on `github Pages <http://courseportal.github.io/coursePortal/>`_.
	*	Started documenting what I have been working on