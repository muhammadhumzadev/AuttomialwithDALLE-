#Docker
# Use an official Python base image from the Docker Hub
FROM python:3.10-slim

# Install necessary packages
RUN apt-get update && \
    apt-get install -y python3-pip

# Set working directory
ENV APP_HOME /project/
WORKDIR $APP_HOME
COPY . /project/

# Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt


#copy migrations
RUN export PATH="/root/.local/bin:$PATH" && \
    python emfetch.py
RUN export PATH="/root/.local/bin:$PATH" && \
    python automail.py

# Expose the port
EXPOSE 3000
