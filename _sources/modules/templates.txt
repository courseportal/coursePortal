.. _templates:

=========
Templates
=========

The template system for knoatom uses bootstrap 2.0.  We have one base template that should be extended by every other template at some degree.  The top of all the templates in web tell you what context variables are required to be set for correct rendering, and which ones are optional.  It also tells you what blocks you can override from ``base.html`` or another template that it extends.

Structure
=========

The idea behind the structure of the templates is to seperate as much content as possible from ``base.html`` and make any content that is in it overridable.  ``base.html`` should only be used for the style and theme of the website and every other template should extend it to get that theme.  The structure for web (as of 6/7/2013) is as follows::

	base.html
	  EXTENDED BY:
	    web_base.html
	      INCLUDES:
	        navbar.html
	          INCLUDES:
	            tree_view.html
	        message.html
	      EXTENDED BY:
            account/forgot_password.html
              Includes:
                form_template.html
            account/index.html
              Includes:
                form_template.html
            account/login.html
              Includes:
                form_template.html
            account/register.html
              Includes:
                form_template.html
            admin/batch_add.html
              Includes:
                form_template.html
            admin/videos.html
		    home/home.html
              EXTENDED BY:
                home/post.html
                home/submit.html
                  Includes:
                    form_template.html
                
                home/base/atom.html
                  INCLUDES:
                    home/shared/atom.html
                      INCLUDES:
                        home/shared/content.html
                          INCLUDES:
                            home/shared/videos.html
                            home/shared/expos.html
                            home/shared/lectureNote.html
                            home/shared/atomDisplay.html
                home/class/atom.html
                INCLUDES:
                  home/shared/atom.html
                    INCLUDES:
                      home/shared/content.html
                        INCLUDES:
                          home/shared/videos.html
                          home/shared/expos.html
                          home/shared/lectureNote.html
                          home/shared/atomDisplay.html
                          
                
                home/base/category.html
                  INCLUDES:
                    home/shared/category.html
                      INCLUDES:
                        home/shared/content.html
                          INCLUDES:
                            home/shared/videos.html
                            home/shared/expos.html
                            home/shared/lectureNote.html
                            home/shared/atomDisplay.html
                            
                home/class/category.html
                INCLUDES:
                  home/shared/category.html
                    INCLUDES:
                      home/shared/content.html
                        INCLUDES:
                          home/shared/videos.html
                          home/shared/expos.html
                          home/shared/lectureNote.html
                          home/shared/atomDisplay.html
                          
                      
                home/base/index.html
                  INCLUDES:
                    home/shared/index.html
                      INCLUDES:
                        top_ratings.html
                home/class/index.html
                INCLUDES:
                  home/shared/index.html
                      INCLUDES:
                        top_ratings.html
                        
It might be a little hard to read because of how many files there are, but there are a lot of patterns and repeated files.

Template Writing Guide
======================

*   There should be **NO** special content in ``base.html``.  The only possible content that should go there is extremely default content or content that is **site wide**.  Any content that goes in ``base.html`` should **always** be overridable by putting it in blocks.
*   ``base.html`` should contain all the style of the site and is where the majority of the html code should go.  The style of the site should be as uniform as possible, and this is why it goes in ``base.html``
*   Follow django's main principle, don't repeat yourself.  Django's template system is really well designed, so take advantage of it.  Never write code twice, that makes it twice as hard to change when you need to change it.  Whenever two places need the same code abstract it by including or extending it.
*   Each section should contain its own "base" template which everything in its app extends.  For instance in ``web``, everything extends ``web_home.html`` which implements the messaging system, and everything that needs a category list extends ``home.html`` which implements the category list for everything else.  An example of a place where you should use include is for the class and base atom templates.  These templates are the same right now, but since they might change in the future I created seperate templates and put all of the shared code in an included file that both of them include.
*   Try your best to follow the style that is already implemented because consistent code is much easier to read.
*   Document your changes as much as possible so others can understand your code