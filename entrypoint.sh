#!/bin/sh
python manage.py makemigrations usrapp
python manage.py makemigrations price
python manage.py makemigrations notifications
python manage.py migrate
echo "Migration is finished !"