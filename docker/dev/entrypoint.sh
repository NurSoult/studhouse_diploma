#!/bin/sh

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py runserver 127.0.0.1:8000