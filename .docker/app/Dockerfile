FROM python:3.10-slim

RUN pip install aiomysql

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./
COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
RUN apt-get update && apt-get install

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]