# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV PORT 8080

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
ENV PIP_ROOT_USER_ACTION=ignore
# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt
#locale
#FROM debian:latest
#RUN apt-get update
#RUN apt-get install -y locales locales-all
#ENV LC_ALL tr_TR.UTF-8
#ENV LANG tr_TR.UTF-8
#ENV LANGUAGE tr_TR.UTF-8

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app