# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make port 5000 available to the world outside this container
# Note: Back4App uses the PORT environment variable
EXPOSE 5000

# Run uvicorn when the container launches
# We use --host 0.0.0.0 to make it accessible outside the container
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
