#!/bin/sh

python manage.py makemigrations
python manage.py migrate
gunicorn Mates.asgi:application -k uvicorn.workers.UvicornWorker -w 2 --bind 0.0.0.0:8000