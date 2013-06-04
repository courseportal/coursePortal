.. _log_nick:

======================
Nick's Development Log
======================

.. contents:: Table of Contents
	:local:

This is where I will keep a log of what I'm working on, problems I'm having, or just notes in general.

Week of June 3-7
================

This week I want to mess around with the orginazational system a little bit to reflect what we discussed in the :ref:`Meeting on 5/7/2013<meeting_notes_5_31_2013>`.

I also want to work on implementing a forum with one "board" for each atom

I also want to start writing documentation for the whole project and start breaking up web into multiple smaller apps so that the project will scale well.

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