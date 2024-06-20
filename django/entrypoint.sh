#!/bin/bash
``
# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate


# Start the server
exec "$@"
