FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VENV_IN_PROJECT=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache



WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN mkdir -p staticfiles media

RUN python manage.py collectstatic --noinput

RUN mkdir -p /app/data && chmod 755 /app/data

RUN python manage.py migrate

RUN python manage.py makemigrations booking

RUN python manage.py migrate

RUN python manage.py generate_sample_data --hotels 1000

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]