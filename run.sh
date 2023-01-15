#!/bin/sh

docker build -t scheduled-ecs .
docker run -v ~/.aws/:/root/.aws:ro scheduled-ecs -e AWS_PROFILE=default
docker run scheduled-ecs