#!/bin/bash

# Verify that entrypoint.sh is in the correct location and executable
ls

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the server
exec "$@"

