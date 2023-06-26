#!/bin/bash
set -e

echo "Applying migrations"

#  this command we create tables and their relationships for the database
python manage.py makemigrations

# transferring the structure to the database
python manage.py migrate

# create superuser for working with http://127.0.0.1:8000/admin
python manage.py createsuperuser_if_none_exists --user=admin --password=adminflora
#echo "Collecting static"
#python manage.py collectstatic --noinput

# initialization  new_database initial_data_for_database.json
python manage.py loaddata new_database.json

echo "Starting app"
python manage.py runserver 0.0.0.0:8000