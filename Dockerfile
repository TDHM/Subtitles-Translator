# syntax=docker/dockerfile:1

FROM google/cloud-sdk:latest

RUN gsutil cp gs://opus-mt-model/en_fr/ en_fr_dl/

FROM python:3.10-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# We don't need a virtualenv since Docker is already isolated
ENV POETRY_VERSION=1.4 \
    POETRY_VIRTUALENVS_CREATE=false

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry install --no-interaction --no-ansi --no-root --no-dev

# Copy Python code to the Docker image
COPY subtitles_translator /code/subtitles_translator/

# Copy model downloaded from GCS
COPY --from=0 en_fr_dl/ en_fr_dl/

# Open the port used by the API
EXPOSE 8000

CMD [ "uvicorn", "subtitles_translator/api_translate:app"]
