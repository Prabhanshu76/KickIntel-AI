# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install any needed packages
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the app for production
RUN npm run build

# Use an official Nginx image to serve the static files
FROM nginx:alpine

# Copy the build files to the Nginx directory
COPY --from=0 /app/build /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Run Nginx
CMD ["nginx", "-g", "daemon off;"]
