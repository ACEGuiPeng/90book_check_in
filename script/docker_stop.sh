#!/usr/bin/env bash
DOCKER_CONTAINER_NAME=90_check_in

echo "try to stop $DOCKER_CONTAINER_NAME"
sudo docker stop ${DOCKER_CONTAINER_NAME}
echo "success to stop $DOCKER_CONTAINER_NAME"