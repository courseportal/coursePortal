#!/bin/bash

cd ../

# move stuff to web directory
cp -R * /var/www/knoatom-web/

# remove .git directory from deployment
rm -rf /var/www/knoatom-web/.git

cd /var/www/knoatom-web

# restore settings file
cp /var/www/knoatom-backup/settings.py knoatom/

# collect static stuff
python manage.py collectstatic --noinput

# sync db
python manage.py syncdb --noinput

# restart apache
service apache2 restart
