FROM python:3.8.3-slim-buster

# COPY linebot.py /app/linebot.py
# COPY requirements.txt /app/requirements.txt

# COPY ./flask/linebot.py ./flask/.env ./flask/requirements.txt /app/
COPY app.py .env requirements.txt /app/

WORKDIR /app/

RUN pip install -r requirements.txt

# RUN pip install line-bot-sdk flask

CMD [ "python","app.py" ]

# RUN python app.py