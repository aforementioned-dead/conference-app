FROM python:3.11.8

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    gcc \
    libffi-dev \
    python3-dev

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install poetry

RUN poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

COPY .env .env

RUN poetry install

ENV DATABASE_URL=${DATABASE_URL}

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]