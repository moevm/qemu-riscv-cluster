#!/bin/bash

docker-compose -f client/docker-compose.yml down

docker-compose -f log_service/docker-compose-logging.yml down

docker network rm logging_public