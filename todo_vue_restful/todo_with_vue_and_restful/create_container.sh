#!/bin/bash

source ./environments.sh

CONTAINER_NAME=$(basename $(PWD))

docker container run -dit -w /usr/src/app --name $CONTAINER_NAME --mount \
    "type=bind,source=$(PWD),target=/usr/src/app" \
    -p $DJANGO_HOST_PORT:$DJANGO_PORT django-base /bin/bash
