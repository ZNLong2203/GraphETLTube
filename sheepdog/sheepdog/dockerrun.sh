#!/bin/bash
set -e

# Run database migrations
alembic upgrade head || flask db upgrade

# Start the application
uwsgi --ini /etc/uwsgi/uwsgi.ini
