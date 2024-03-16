# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Specify the command to run on container startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
