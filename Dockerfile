FROM python:3.13.7-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean



WORKDIR /app

ENV PYTHONPATH=/app

ENV TZ=Europe/Berlin

COPY requirements.txt .

COPY logging_config.json .

COPY pyproject.toml .

RUN mkdir -p /var/log && touch /var/log/cron.log && chmod 0666 /var/log/cron.log

RUN pip install --no-cache-dir -r requirements.txt

USER root

COPY . .
COPY scripts /scripts 

RUN chmod +x /scripts/*.sh



ENTRYPOINT ["/scripts/entrypoint.sh"]
