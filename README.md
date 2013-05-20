# Knoatom

## Pre-requisites

* mysql database (you're on your own for this one)
* pip (for installing various python things)

        apt-get install python-pip python-dev build-essential

* django (python web framework)

        pip install django

* mysql-python (this is probably the trickiest one to install)

        pip install mysql-python

## Initial Setup

For an initial setup of knoatom-web, here's some of the things you need to do:

1. Clone and move into the repository
2. Copy `settings-example.py` to `settings.py` and set the various things that are required in it:
    * In the `DATABASES.default` dictionary, set
        * `NAME` - name of your database
        * `USER` - user for your database
        * `PASSWORD` - password for your user
    * `MEDIA_ROOT` - file system location for uploaded files
    * `MEDIA_URL` - url for getting to `MEDIA_ROOT`
    * `STATIC_ROOT` - file system location for static files (will be collected here)
    * `STATIC_URL` - url for getting to `STATIC_ROOT`
    * `ADMIN_MEDIA_PREFIX` - typically the value of `STATIC_URL` + `admin/`
    * `SECRET_KEY` - longer the better - [random.org](http://www.random.org/strings/) will help you out)
3. Set up your database running the following commands (errors in these will probably be fixed by reading the errors and adjusting `settings.py`):
    * `./manage.py syncdb` - creates the database tables and initial user
    * `./manage.py loaddata web/fixtures/web_init_categories.json` - installs initial data
4. Cross your fingers, and run the server:

        ./manage.py runserver 8080

5. Open the url [http://localhost:8080](http://localhost:8080) and hopefully you'll see it (if you're running on your local machine).

### Installing Initial Categories

To bring in the initial categories into the database, you need to provide a 'fixture' that contains the data. To bring in the initial categories from `web_init_categories.json` do:

    ./manage.py loaddata web/fixtures/web_init_categories.json

### Creating Fixtures

You can read more about this in the South documentation, but it is more or less this:

    ./manage.py dumpdata web > web.json

`web` referring to the application that is set up in django (`web` is what ours is). This outputs the fixture to `web.json`, rather than print it to the screen.

You can omit the web to dump all the data from the database.
