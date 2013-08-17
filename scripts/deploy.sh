#!/bin/bash

PROJECT_ROOT="/var/www/knoatom-web/"
APACHE2_DIR="/etc/apache2/"
BACKUP_ROOT="/var/www/knoatom-web-backup/"
SETTINGS="knoatom.settings.production"
APPS=( "knoatom" "web" "assignment" "rating" "pybb" "haystack" )
echo "Variables set"
cd ../ # cd into git project root
# Copy contents of project root
cp -rf $PROJECT_ROOT* $BACKUP_ROOT
echo "Backed up the code that is currently in $PROJECT_ROOT"
# Delete contents of project root
rm -rf $PROJECT_ROOT*
echo "Deleted code in $PROJECT_ROOT"
# copy to project root
cp -r * $PROJECT_ROOT
echo "Copied code from current directory into $PROJECT_ROOT"
# cd into project root
cd $PROJECT_ROOT
# Delete .git* files and secret_key.py
rm -rf .git .gitignore knoatom/settings/secret_key.py
echo "Deleted unwanted files."
# Upgrade python packages, does not include MySql-Python! Must have pip
pip install ../dependencies.txt --upgrade
echo "Installed and upgraded all dependencies."
# collect static stuff
python manage.py collectstatic --settings=$SETTINGS --noinput
echo "Collected static files"
# sync db, we NEED to work on creating south migrations correctly
for i in ${APPS[@]}
do
        python manage.py migrate $i --settings=$SETTINGS
done
echo "Migrated all APPS"
#python manage.py syncdb --noinput

# restart apache
sudo service apache2 restart
echo "Restarted server"
echo "Done"