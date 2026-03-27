#!/bin/bash

# 1. Start MongoDB in the background (Self-Sustained Mode for VPS)
echo "Initializing and starting local MongoDB database..."
mkdir -p /data/db
mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db --bind_ip 127.0.0.1

# 2. Start Nginx in the background (Listening on Port 8077)
echo "Starting Nginx reverse proxy on port 8077..."
nginx -g "daemon off;" &

# 3. Start the FastAPI backend on localhost:8000
echo "Starting Python FastAPI backend..."
uvicorn app.main:app --host 127.0.0.1 --port 8000
