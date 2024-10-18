#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Make migrations for the LesProduits app
python3 manage.py makemigrations LesProduits

# Generate the SQL for the initial migration
python3 manage.py sqlmigrate LesProduits 0003

# Apply the migrations
python3 manage.py migrate

# Load initial data from the fixture
python3 manage.py loaddata init_data.json

echo "Database setup completed successfully."