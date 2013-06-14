.. _log_nick:

======================
Nick's Development Log
======================

.. contents:: Table of Contents
	:local:

This is where I will keep a log of what I'm working on, problems I'm having, or just notes in general.

Week of June 10-15
==================

So far this week so far I have:
    *   Fixed the forum poll system
    *   Added the ability for all users to submit new content for:
    
            -   Expositions
            -   Lecture Notes
            -   Examples
        
        Lecture Notes and Examples are limited to ``.pdf`` files right now.
    *   I have been adding documentation as I go to various functions and classes.
    *   Added the ability for the owner of a user submitted object and all staff/superusers to edit/delete that object where they are listed.  This works for:
        
            -   Expositions
            -   Lecture Notes
            -   Examples
            -   Videos
    
    *   Improved aesthetics of exposition/note/example display list

Goals
-----

This week I'm working on fully integrating the forums into the website as well as improving the user upload system and then if there is time adding a vote system to the forums and user uploads.  The following todo list will probably take more than 1 week to implement

Todo:
    *   Get forum poll system working (Done!)
    *   Integrate forum into the Atom better
    *   Add functionality to submit new content for:
            -   Expositions(Done!)
            -   Lecture Notes(Done!)
            -   Examples(Done!)
    *   Add functionality to edit/delete content you submitted for:
            -   Expositions(Done!)
            -   Lecture Notes(Done!)
            -   Examples(Done!)
            -   Videos(Done!)
    *   Check to see if the profile image in the forums works(Done!)
    *   Put a delete option in the submit form if they are editing
    *   Add a report feature for all content/posts so that malicious/disrespectful content can be removed
    *   Allow professors to "sticky" content to stay at the top of the content list no matter the ranking in some way, maybe create a new tab for stickied content.
    *   Implement a vote based ranking system for the forums and for listing content
    *   Give users a rating based on submissions and quality of their submissions and use that rating to give "initial" rating to new content/posts
    *   Submit a bug feature(Done by Taoran!)

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

Goals
-----

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