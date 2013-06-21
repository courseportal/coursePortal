#!/bin/bash
# Search script

./manage.py build_solr_schema > solr-4.3.0/example/solr/collection1/conf/schema.xml

./modifySchema.py

cd solr-4.3.0/example/

./startSearchEngine.sh &

python ../../manage.py rebuild_index

python ../../manage.py runserver




