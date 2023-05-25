# Use an official Node.js runtime as the base image
FROM node:12-alpine

# Set the working directory in the container
WORKDIR /app
ENV NODE_OPTIONS=--max_old_space_size=8196

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the application code to the container
COPY . .

# Build the React app
RUN npm run build

# Set the environment variable for the production build
ENV NODE_ENV=production

# Expose the port that the app will run on
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
