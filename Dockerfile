FROM python:3.13.7-slim

ENV DEBIAN_FRONTEND=noninteractive

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && \
    apt-get install -y \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean



WORKDIR /app

COPY pyproject.toml .
COPY uv.lock* .

RUN uv sync --frozen

ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

ENV TZ=Europe/Berlin

COPY logging_config.json .


RUN mkdir -p /var/log && touch /var/log/cron.log && chmod 0666 /var/log/cron.log

USER root

COPY . .
COPY scripts /scripts 

RUN chmod +x /scripts/*.sh



ENTRYPOINT ["/scripts/entrypoint.sh"]
