#!/bin/bash
# Exit immediately if a command fails
set -e

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Compile translations
echo "Compiling messages..."
python manage.py compilemessages

# Start Supervisor (or your app)
exec "$@"
