#!/bin/bash

SERVICE=$(basename $(PWD))

docker container start $SERVICE -ai
