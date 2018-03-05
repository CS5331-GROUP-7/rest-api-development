#!/bin/bash
set -e
sudo docker-compose -f docker-compose-test.yml -p test build
sudo docker-compose -f docker-compose-test.yml -p test run tests python -m pytest --cov=src/service/ tests
sudo docker stop test_app_1 test_mongodb_1
