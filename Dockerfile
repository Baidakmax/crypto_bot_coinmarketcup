# Using the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy project files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8443 available to the world outside this container
EXPOSE 8443

# Define environment variable
ENV NAME World

# The command to start the bot
CMD ["python", "bot.py"]

