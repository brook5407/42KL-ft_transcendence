#!/bin/bash

RUN_PORT="${PORT:-8000}"
DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-admin}"
DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-admin@example.com}"
DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-adminpassword}"

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Create superuser if DJANGO_SUPERUSER_CREATE is set to 'true'
if [ "$DJANGO_SUPERUSER_CREATE" = "true" ]; then
    python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
fi

# Start the server
daphne -b 0.0.0.0 -p $RUN_PORT core.asgi:application