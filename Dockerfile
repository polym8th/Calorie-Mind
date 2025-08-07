# Use Node.js base image with Debian (for apt-get)
FROM node:18-bullseye

# Set working directory inside container
WORKDIR /app

# Install Python and build tools for node-gyp
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    && apt-get clean

# Set PYTHON environment variable for node-gyp
ENV PYTHON=/usr/bin/python3

# Copy package files first to install dependencies
COPY package*.json ./

# Install dependencies (respects package-lock.json if present)
RUN npm ci

# Copy the rest of the app
COPY . .

# Set the default command to run your app
CMD ["npm", "start"]
