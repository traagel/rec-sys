# Use an official MongoDB runtime as a parent image
FROM mongo:4.4-bionic

# Set environment variables (replace with your own names)
ENV MONGO_INITDB_DATABASE=proc-rec-db
ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=password

# Copy your data file into the Docker image
COPY data/dataset_engineer.json /data/dataset_engineer.json

# Copy the script into the Docker image
COPY mongo_script.sh /docker-entrypoint-initdb.d/

# Copy the script to create user into the Docker image
COPY mongo_create_user.sh /docker-entrypoint-initdb.d/

# Make the scripts executable
RUN chmod +x /docker-entrypoint-initdb.d/mongo_script.sh
RUN chmod +x /docker-entrypoint-initdb.d/mongo_create_user.sh

# Expose the port MongoDB uses. This tells Docker that the container listens on the specified network ports at runtime.
EXPOSE 27017

