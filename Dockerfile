FROM python:3.11-buster

RUN pip install poetry==1.4.2

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY mSteaming ./mSteaming

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]
