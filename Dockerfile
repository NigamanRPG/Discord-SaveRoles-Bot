FROM python:latest

WORKDIR /usr/src/app

COPY . .
RUN python3 -m pip install --no-cache-dir -r ./requirements.txt

VOLUME /usr/src/app/config

CMD ["python3", "./bot.py"]
