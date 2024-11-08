# syntax=docker/dockerfile:1

# Base python image for custom image
FROM python:3.9.13-slim-buster

RUN apt-get update && \
    apt-get install -y \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*
# Create working directory and install pip dependencies
WORKDIR /GANS-GENS
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --ignore-installed --no-deps

COPY . .

# Define environment variable
ENV NAME World
# Run the server using app.py
CMD ["python3", "main.py"]