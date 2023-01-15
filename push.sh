#!/bin/bash

export AWS_SHARED_CREDENTIALS_FILE="$HOME/.aws/credentials"
repo="$(cat repo)"
uri="$(cat uri)"

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $uri
docker buildx build --platform=linux/amd64 -t scheduled-ecs .
docker tag scheduled-ecs:latest "$repo"\:latest
docker push "$repo"\:latest