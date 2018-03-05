#!/bin/bash
set -e
sudo docker-compose -f docker-compose-test.yml -p test build

sudo docker-compose -f docker-compose-test.yml -p test run tests python drop_db.py 
sudo docker-compose -f docker-compose-test.yml -p test run tests python -m py.test --cov=src/service/ tests
sudo docker stop test_app_1 test_mongodb_1
