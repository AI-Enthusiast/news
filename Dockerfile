# Use the official lightweight Python image based on Debian
FROM python:3.12.9

# Set the working directory
WORKDIR /news

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "src/scraper.py"]