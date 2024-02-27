FROM python:3.12.2-alpine3.19

# Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1

# Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1

# create root directory for our project in the container
RUN mkdir /dist
WORKDIR /dist

# create content directory for logging
RUN mkdir /dist/contents

ADD ./src /dist/src
ADD ./.gitlab-ci.yml /dist/.gitlab-ci.yml
ADD ./requirements.txt /dist/requirements.txt
ADD ./env/example.env /dist/.env

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Remove temporarily lib for building the python package 
RUN rm -rf /tmp/*

WORKDIR /dist/src
CMD ["python", "app.py"]
