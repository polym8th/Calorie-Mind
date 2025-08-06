# Base image with Node.js and Linux tools
FROM node:18

# Install Python and build tools
RUN apt-get update && apt-get install -y python3 make g++ \
    && npm install -g npm@latest

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies
RUN npm ci

# Expose your app's port
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
