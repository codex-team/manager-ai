FROM python:3.6

COPY . .
VOLUME ./logs/:./logs/
RUN pip install -r requirements.txt

EXPOSE 8000
