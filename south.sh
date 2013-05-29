#!/bin/sh
# This runs south

#------------Instructions------------#
#The first argument is requied and must be either -migrate or -setup.
#Use -migrate when you want to migrate an app that is already setup, and
#-setup to setup an app to migrate.
#
#The second argument is optional, which is -print. This tag must go after 
#[-migrate/-setup] but before any other arguments.  If this tag is set then
#instead of executing the [setup/migration] it just prints out the commands
#it would have used to [setup/migrate].  If this tag is not set then it will
#run the commands.
#
#The rest of the arguments are the names of the apps that you want to
#[setup/migrate].
#
#Here are a few examples:
#./south.sh -setup myapp myapp2
#./south.sh -setup -print myapp myapp2 myapp3
#./south.sh -migrate myapp myapp2
#./south.sh -migrate -print myapp

if [ "$1" == "-migrate" ]
then
    echo "Migrating"
    for app in "$@"
    do
        if [ "$2" != "-print" ]
        then
            if [ "$app" != "-migrate" -a "$app" != "-print" ]
            then
                ./manage.py schemamigration "$app" --auto
                ./manage.py migrate "$app"
            fi
        else
            if [ "$app" != "-migrate" -a "$app" != "-print" ]
            then
                echo ./manage.py schemamigration "$app" --auto
                echo ./manage.py migrate "$app"
            fi
        fi
    done
fi

if [ "$1" == "-setup" ]
then
    echo "Setting up"
    if [ "$2" != "-print" ]
    then
        ./manage.py syncdb
    else
        echo ./manage.py syncdb
    fi
    for app in "$@"
    do
        if [ "$2" != "-print" ]
        then
            if [ "$app" != "-setup" -a "$app" != "-print" ]
            then
                ./manage.py schemamigration "$app" --initial
                ./manage.py migrate "$app" --fake
            fi
        else
            if [ "$app" != "-setup" -a "$app" != "-print" ]
            then
                echo ./manage.py schemamigration "$app" --initial
                echo ./manage.py migrate "$app" --fake
            fi
        fi
    done
    
    
fi