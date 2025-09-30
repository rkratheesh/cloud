#!/bin/bash
set -e

# Create migrations for all apps
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static
python manage.py collectstatic --noinput

# Compile translations
python manage.py compilemessages

# Start Supervisor
exec "$@"
