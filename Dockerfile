# Using alpine image
FROM python:3.9-alpine

# Installing packages
RUN apk --update --no-cache add python3-dev libffi-dev gcc musl-dev make libevent-dev build-base
RUN pip install --no-cache-dir pipenv

# Defining working directory
WORKDIR /usr/src/app

# Adding source code
COPY . /usr/src/app/
RUN chmod 755 bootstrap.sh
COPY Engine/ ./Engine

#Install API dependencies
RUN pipenv install

ENV PYTHONPATH="/usr/src/app/Engine"

#START APP AND SERVERS
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]