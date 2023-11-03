#!/bin/bash

# Utility script to stop and delete containers and volumes

# Get current folder name
current_folder=$(basename $(pwd))
echo $current_folder

# Stop containers
docker-compose down

# Delete web_interface image
docker rmi ${current_folder}-web_access

# Delete web_interface volume
docker volume rm ${current_folder}_web-data

