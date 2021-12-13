FROM python:3.9-slim-bullseye

COPY requirements.txt /tmp/
RUN pip install -U pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt
ADD bot/bot.py bot/bot.py
ADD bot/sm.py bot/sm.py
ENTRYPOINT ["python", "bot/bot.py"]
