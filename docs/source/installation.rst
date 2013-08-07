.. _installation:

============
Installation
============

This document will provide detailed instructions on how to install knoatom onto your computer and get the site fully functional.  

Step-by-Step Installation Guide
===============================

Following these steps will fully setup your machine to run knoatom.  This guide is written for Mac/linux, so the installation on windows might vary.

Pip
---

The first step is to install ``pip``.  ``pip`` allows you to easily install other python packages.

a) Download and instal setuptools from `here <https://pypi.python.org/pypi/setuptools>`_ following the instructions.
	
b) Install ``pip``::

	$ easy_install pip
		
MySQL
-----
Next we will install MySQL and setup knoatom's database.  First download the MySQL disk image (``mysql-5.6.11-osx10.7-x86.dmg``) from their `website <http://dev.mysql.com/downloads/mysql/>`_ and follow the instructions to install it.

Now we need to create the database used for knoatom.  First ``cd`` into ``local`` and run MySQL::

	$ cd /usr/local/mysql
	$ ./mysql -u root
	
The MySQL command line should now be displayed in your terminal.  Next type the following MySQL commands::

	mysql> CREATE DATABASE knoatom;
	mysql> GRANT USAGE ON *.* TO knoatom@localhost identified by password;
	mysql> GRANT ALL PRIVILEGS ON knoatom.* TO knoatom@localhost;
	
Now you can exit MySQL if you want by entering ``^D``.
	
Virtualenv
----------
	  
The next thing you should install is ``virtualenv`` and ``virtualenvwrapper``.  While this isn't neccessary, it prevents conflicts and keeps your working enviroment isolated. Install them using these commands::

	$ pip install virtualenv
	$ pip install virtualenvwrapper
	
Now you need to setup ``virtualenvwrapper``. You need to edit one of [``~/.bash_profile`` / ``~/.bashrc`` / ``~/.profile`` / ect.] depending on which one you see in your ``~/`` directory (e.g. vim ``~/.bash_profile`` or your favorite editor).  Add the following three lines to your shell startup file:

.. code-block:: sh

	export WORKON_HOME=$HOME/.envs
	export PROJECT_HOME=$HOME/Projects
	source /Library/Frameworks/Python.framework/Versions/2.7/bin/virtualenvwrapper.sh
	
.. note::
	
	If there is no file at ``/Library/Frameworks/Python.framework/Versions/2.7/bin/virtualenvwrapper.sh`` then your pip installs to a different location.  You need to find  ``/path/to/virtualenvwrapper.sh``.
	
Then reload the startup file, (e.g. run ``source ~/.bash_prifle``)

	
	
After you have installed and setup ``virtualenv`` you must cd into your working directory and run the these commands to start using your virtual environment::

	$ mkvirtualenv <venv_name>
	$ workon <venv_name>
	
.. note::	
	
	You can run ``deactivate`` to leave the virtual environment and return to your normal environment.  Full documentation can be found on their `site <http://virtualenvwrapper.readthedocs.org/en/latest/>`_.
	
	You can pick anything as your ``<venv_name>``.
	
MySQL-Python
------------

Now here comes the hardest part, installing mysql-python.  It is important that if you are going to use virtualenv that you are in your virtual environment.  Your command line prompt should look like ``(<venv_name>)$``.  Follow these steps **exactly** and you probably won't have any problems.
	
a.	Download `MySQL-python-1.2.3.tar.gz <ttp://sourceforge.net/projects/mysql-python/files/mysql-python/1.2.2/>`_.
	
b.	Extract the package (Just click on it).
c.	``cd`` into the extracted folder and edit ``setup_posix.py``.  Change

	.. code-block:: python
	
		mysql_config.path = "mysql_config"
		
	to
	
	.. code-block:: python
	
		mysql_config.path = "/usr/local/mysql/bin/mysql_config"
		
d.	The next thing you need to do is change your ``mysql_config`` file::

		(<venv_name>)$ cd /usr/local/mysql/bin/mysql_config
	
	Now change lines 119 and 120 from
	
	.. code-block:: sh
	
		cflags="-I$pkgincludedir  -Wall -Wno-null-conversion -Wno-unused-private-field -Os -g -fno-strict-aliasing -DDBUG_OFF -arch x86_64 " #note: end space!
		cxxflags="-I$pkgincludedir  -Wall -Wno-null-conversion -Wno-unused-private-field -Os -g -fno-strict-aliasing -DDBUG_OFF -arch x86_64 " #note: end space!
		
	to
	
	.. code-block:: sh
	
		cflags="-I$pkgincludedir  -Wall -Os -g -fno-strict-aliasing -DDBUG_OFF -arch x86_64 " #note: end space!
		cxxflags="-I$pkgincludedir  -Os -g -fno-strict-aliasing -DDBUG_OFF -arch x86_64 " #note: end space!
		
e.	Create a sybmolic link::

		(<venv_name>)$ sudo ln -s /usr/local/mysql/lib /usr/local/mysql/lib/mysql
		
f.	Clean the package (``cd`` back into ``MySQL-python-1.2.3``)::

		(<venv_name>)$ sudo python setup.py clean
	
g.	The last thing you need to do is build and install::
		
		(<venv_name>)$ sudo python setup.py build
		(<venv_name>)$ sudo python setup.py install

Install Django and Required Apps
--------------------------------

1.	Install django into your virtual environment, which is very simple using pip::
	
		(<venv_name>)$ pip install django
		
2.	Install all of the required apps for knoatom::

		(<venv_name>)$ pip install python-memcached
		(<venv_name>)$ pip install south
		(<venv_name>)$ pip install django_wysiwyg
		(<venv_name>)$ pip install markdown
		(<venv_name>)$ pip install postmarkup
		(<venv_name>)$ pip install django-annoying
		(<venv_name>)$ pip install sorl-thumbnail
		(<venv_name>)$ pip install pil
		(<venv_name>)$ pip install django-pure-pagination
		(<venv_name>)$ pip install sphinx
		(<venv_name>)$ pip install pysolr
		(<venv_name>)$ pip install simplejson
        (<venv_name>)$ pip install numpy
        
        
		
Get Source Code
---------------
		
Now you need to clone the source code from the repository.  The first thing you need to do is ask someone to add you to the orginization on gitHub so you can use the repository.  Then ``cd`` into your working directory and use the following command::

	git clone https://github.com/courseportal/coursePortal.git
	
.. note::

	More detailed instructions on how to use git can be found **HERE (LINK THIS!!!)**.
	
Setup Database
--------------
		
1.	Sync your database and set it up for south migration using the folloing command::

		(<venv_name>)$ python manage.py syncdb --all
		(<venv_name>)$ python manage.py migrate web assignment pybb --fake
		
		
2.	If there is a current fixture in ``web/fixtures/`` then you can load it using the following command::

	(<venv_name>)$ ./manage.py loaddata web/fixtures/<fixture_name>.json
	
10.	Everything should be working now, check that it is by running the command::

		(<venv_name>)$ ./manage.py runserver
		
	and make sure everything is working
    
About Search with Solr
----------------------

1. Start the Solr Search Engine (under the folder with your picked <venv_name> )::
    
   
   $ cd solr-4.3.0/example
   $ java -jar start.jar

2. Manually rebuild the index if necessary (If items have been created or documents have been uploaded before the Solr Search Engine starts, this step is necessary) ::

   (<venv_name>)$ ./manage.py rebuild_index
   
3. If no error throws up in step 2, everything should be working now, check by running the server again::

    (<venv_name>)$ ./manage.py runserver
