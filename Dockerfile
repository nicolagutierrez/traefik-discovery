FROM python:3.9-slim

WORKDIR /app

ARG HOMEPAGE_PATH
ARG TRAEFIK_PATH

COPY ./src /app
COPY requirements.txt /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set environment variables
ENV HOMEPAGE_PATH=$HOMEPAGE_PATH
ENV TRAEFIK_PATH=$TRAEFIK_PATH

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
