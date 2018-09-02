#!/usr/bin/env bash
PROJECT_PATH=$(cd "$(dirname "$0")";cd ..;pwd)
# settings
DOCKER_PROJECT_PATH=/project
DOCKER_CONTAINER_NAME=90_check_in
DOCKER_IMAGE_NAME=${DOCKER_CONTAINER_NAME}:v1

echo "project path is $PROJECT_PATH,start to run..."
sudo docker stop ${DOCKER_CONTAINER_NAME}
sudo docker rm ${DOCKER_CONTAINER_NAME}
sudo docker run --name ${DOCKER_CONTAINER_NAME} -d -e "PYTHONPATH=$DOCKER_PROJECT_PATH"   --log-opt max-size=50m --log-opt max-file=5 ${DOCKER_IMAGE_NAME}
sudo docker logs -f ${DOCKER_CONTAINER_NAME}