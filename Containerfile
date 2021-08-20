FROM python:3.9-slim-bullseye

COPY requirements.txt /tmp/
RUN pip install -U pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt
ADD bot bot
ENTRYPOINT ["python", "bot/bot.py"]
