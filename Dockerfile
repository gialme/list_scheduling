# Start from the official Python image
FROM python:latest

# Create a directory for the application
WORKDIR /app

# Copy the .whl file into the container
COPY ./dist/list_scheduling-1.0.0-py3-none-any.whl .

# Copy the example input file into the container
#COPY ./examples/example_config.txt /app/

# Install the package using pip
RUN python -m pip install list_scheduling-1.0.0-py3-none-any.whl

# Set the entrypoint to execute the package
ENTRYPOINT ["list_scheduling"]