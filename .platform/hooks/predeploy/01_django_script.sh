#!/bin/bash

source /var/app/venv/*/bin/activate
cd /var/app/staging

# migrations
python manage.py makemigrations
python manage.py migrate

# create superuser
python manage.py createsu

# messages
python manage.py makemessages --locale=ko
python manage.py compilemessages

# static
python manage.py collectstatic --noinput