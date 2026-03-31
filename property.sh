#!/bin/bash
# set -e
# cd /var/www/property
# source venv/bin/activate
# Load environment variables from .env
# export $(grep -v '^#' .env | xargs)
# Run your script first
# python app/scripts/add_country.py
# Start the app
# exec uvicorn app.main:app --host 0.0.0.0 --port 3001



#!/bin/bash
set -e

# Move to project root
cd /var/www/property

# Activate virtual environment
source venv/bin/activate

# Ensure Python sees the project root as a module
export PYTHONPATH=$(pwd)

# Run your script as a module
# python -m app.scripts.add_country

# Start the app
exec uvicorn app.main:app --host 0.0.0.0 --port 3001
