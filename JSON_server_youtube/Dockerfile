# Use the official image as a parent image.
FROM node:latest

# Set the working directory.
WORKDIR /usr/src/app

# Copy the file from your host to your current location.
COPY package.json .

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 3000

EXPOSE 9999

# RUN [ "echo", "nameserver", "8.8.8.8", ">", "/etc/resolv.conf"]
# RUN [ "apt-get", "update"]
# RUN [ "apt-get", "install", "-y", "net-tools"]


# Run the specified command within the container.
# CMD [ "node", "transferRequest.js", "&&", "node", "control_server.js"]
CMD sh start.sh

# build command 
# docker build --tag bulletinboard:1.0 .
