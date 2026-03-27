# Stage 1: Build the frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
# Cache dependencies
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Final runtime image
FROM node:20-alpine
WORKDIR /app

# Set production environment
ENV NODE_ENV=production
# CodeHost provides the PORT variable; we default to 3001 for local testing
ENV PORT=3001

# Copy backend source and install production-only dependencies
COPY backend/package*.json ./backend/
WORKDIR /app/backend
RUN npm install --production
COPY backend/ .

# Copy built frontend to the expected location for the Node server
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Memory optimization for CodeHost's 128MB RAM limit
# --max-old-space-size=96 limits Node's heap to ~96MB
ENV NODE_OPTIONS="--max-old-space-size=96"

# Command to start the application
CMD ["node", "server.js"]
