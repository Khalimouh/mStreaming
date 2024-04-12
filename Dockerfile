FROM python:3.11.6-slim-bookworm

RUN pip install poetry==1.2.0
RUN apt update -y

COPY . /mStreaming

WORKDIR /mStreaming
RUN poetry install --without dev

WORKDIR /mStreaming
ENTRYPOINT ["poetry", "run", "uvicorn","main:app", "--reload"]
