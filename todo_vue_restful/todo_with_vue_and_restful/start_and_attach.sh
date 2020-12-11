#!/bin/bash

source ./environments.sh

SERVICE=$(basename $(PWD))

if [ $# -ge 1 ];
then
    docker container start $SERVICE
    docker container exec -d $SERVICE python manage.py runserver     "0.0.0.0:$DJANGO_PORT"
else
    docker container start $SERVICE -ai
fi
