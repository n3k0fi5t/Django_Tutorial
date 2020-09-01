#!/bin/bash

CONTAINER_NAME=$(basename $(PWD))
HOST_PORT=5004
PORT=8080

#docker container run -d -w /usr/src/app --name $CONTAINER_NAME --mount "type=bind,source=$(PWD),target=/usr/src/app" \
#    -p $HOST_PORT:$PORT django-base python manage.py runserver 0.0.0.0:$PORT

docker container run -dit -w /usr/src/app --name $CONTAINER_NAME --mount "type=bind,source=$(PWD),target=/usr/src/app" \
    -p $HOST_PORT:$PORT django-base /bin/bash
