FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code (this is mostly for production, docker-compose uses volumes for dev)
COPY . .

EXPOSE 5173

# Run Vite dev server, exposed to 0.0.0.0 so Docker can map the port
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
