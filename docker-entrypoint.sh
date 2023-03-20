#!/bin/bash
set -e
sleep 5
# python /app/source/manage.py migrate

exec "$@"