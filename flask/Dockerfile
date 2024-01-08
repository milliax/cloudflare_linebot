FROM python:3.8.3-slim-buster

# COPY linebot.py /app/linebot.py
# COPY requirements.txt /app/requirements.txt

COPY linebot.py .env requirements.txt /api-flask/

WORKDIR /api-flask

RUN pip install -r requirements.txt

RUN python linebot.py