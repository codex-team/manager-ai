FROM python:3.7-alpine

COPY requirements.txt /
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install -r requirements.txt
