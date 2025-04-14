# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Run Flask app
CMD ["python", "server.py"]
