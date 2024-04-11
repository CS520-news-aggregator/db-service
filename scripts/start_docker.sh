#!/bin/bash

docker build . -t db-service

docker run -it --rm --network host db-service