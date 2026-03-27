#!/bin/bash

# Substitute PORT environment variable into Nginx config (envsubst provided by gettext-base)
# The file is expected to be placed at /etc/nginx/conf.d/default.conf.template in the container
envsubst '${PORT}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

# Start Nginx in the background
echo "Starting Nginx on port $PORT..."
nginx -g "daemon off;" &

# Start the FastAPI backend via Uvicorn on localhost:8000
echo "Starting Python FastAPI backend..."
uvicorn app.main:app --host 127.0.0.1 --port 8000
