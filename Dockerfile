# -- Phase 1: Build the React frontend --
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# -- Phase 2: Python backend + Nginx final production image --
FROM python:3.10-slim

# Install system dependencies for OCR, OpenCV and Nginx
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    gettext-base \
    nginx \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python backend dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Copy the frontend built assets from Phase 1 to Nginx distribution folder
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Copy deployment configurations
COPY deployment/nginx_codehost.conf /etc/nginx/conf.d/default.conf.template
COPY deployment/start_codehost.sh /start.sh
RUN chmod +x /start.sh

# CodeHost assigns a dynamic PORT via environment variable
ENV PORT=80
EXPOSE 80

CMD ["/start.sh"]
