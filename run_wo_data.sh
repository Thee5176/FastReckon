#!/usr/bin/bash

docker-compose down
docker volume rm fastreckon_postgres_data
docker-compose up -d --build
docker-compose exec web python manage.py migrate 