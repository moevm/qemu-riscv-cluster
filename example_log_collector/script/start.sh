#!/bin/bash

docker network create logging_public

docker-compose -f log_service/docker-compose-logging.yml up -d

docker-compose -f client/docker-compose.yml up -d