FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# Vite needs to be accessible from outside the container
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
