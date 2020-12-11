#!/bin/bash

source ./environments.sh

python manage.py runserver 0.0.0.0:$DJANGO_PORT

