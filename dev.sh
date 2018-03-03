#!/bin/bash
set -e
sudo docker-compose -f docker-compose-dev.yml build
sudo docker-compose  -f docker-compose-dev.yml up
