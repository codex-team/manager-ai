FROM python:3.7-alpine

RUN apk add --update --no-cache g++ gcc libxslt-dev

COPY requirements.txt /

RUN pip install -r requirements.txt

WORKDIR /home/manager-ai

CMD ["python", "./src/main.py"]