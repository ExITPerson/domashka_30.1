FROM python:3.12-slim

ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv $POETRY_HOME && \
    $POETRY_HOME/bin/pip install poetry==$POETRY_VERSION

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
