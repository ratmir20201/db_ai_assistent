FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /api

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --without dev

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]