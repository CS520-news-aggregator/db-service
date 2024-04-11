#!/bin/bash

docker build . -t db-service

docker run -it -v ${PWD}:/code --rm --network host db-service
