# Use latest Node 22 image
FROM node:22

# Install Python and build tools
RUN apt-get update && apt-get install -y python3 make g++

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN npm install

# Expose port (change this if your app runs on a different one)
EXPOSE 3000

# Start app
CMD ["npm", "start"]
