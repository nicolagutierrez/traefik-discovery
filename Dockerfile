FROM python:3.9-slim

WORKDIR /traefik_dicovery/app

ARG HOMEPAGE_PATH

COPY ./src /traefik_dicovery/app
COPY requirements.txt /traefik_dicovery/app

RUN pip install --trusted-host pypi.python.org -r requirements.txt


ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
