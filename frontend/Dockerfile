# Builder stage for React frontend
FROM node:18-alpine AS builder
WORKDIR /app

# Install dependencies rapidly using cached layers
COPY package*.json ./
RUN npm install

# Build static bundle
COPY . .
RUN npm run build

# Nginx production serve layer
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
