# Use the Python 3 alpine official image
# https://hub.docker.com/_/python
FROM python:3-alpine

# Create and change to the app directory.
WORKDIR /app

# Copy local code to the container image.
#COPY /main.py . /main.py .
COPY /requirements.txt . /requirements.txt .

# Install project dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup.
#CMD ["python3", "main.py"]
