# Using the official Python image
FROM python: 3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy project files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# The command to start the bot
CMD ["python", "bot.py"]

