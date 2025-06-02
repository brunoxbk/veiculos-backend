
FROM python:3.11-slim


WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
         netcat-traditional \
        git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY --chmod=755 entrypoint.sh /code/entrypoint.sh

RUN chmod +x /code/entrypoint.sh

COPY . /code/


RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /code
USER appuser
