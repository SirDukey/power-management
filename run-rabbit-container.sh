#!/bin/bash

CONTAINER_NAME=rabbitmq

if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]
then
  docker container start $CONTAINER_NAME 1> /dev/null
  echo "started container $CONTAINER_NAME"
else
  docker run -d --name $CONTAINER_NAME -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management
fi
