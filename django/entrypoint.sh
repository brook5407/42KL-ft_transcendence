#!/bin/bash

RUN_PORT="${PORT:-8000}"

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Start the server
daphne -b 0.0.0.0 -p $RUN_PORT core.asgi:application
