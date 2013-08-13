#!/bin/bash

PROJECT_ROOT="/var/www/knoatom-web/"
APACHE2_DIR ="/etc/apache2/"
BACKUP_ROOT="/var/www/knoatom-web-backup/"
SETTINGS="knoatom.settings.production"
APPS=( "web" "assignment" "rating" )

cd ../ # cd into git project root
# Pull from github
git pull origin
# Copy contents of project root
cp -rf $PROJECT_ROOT* $BACKUP_ROOT*
# Delete contents of project root
rm -rf $PROJECT_ROOT*
# copy to project root
cp -r * $PROJECT_ROOT
# cd into project root
cd $PROJECT_ROOT
# Delete .git* files and secret_key.py
rm -rf .git .gitignore knoatom/settings/secret_key.py

# collect static stuff
python manage.py collectstatic --settings=$SETTINGS --noinput

# sync db, we NEED to work on creating south migrations correctly
#for i in ${APPS[@]}
#do
#	python manage.py migrate $i --settings=$SETTINGS --noinput
#done
python manage.py syncdb --noinput

# restart apache
service apache2 restart
