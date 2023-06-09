# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

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

CMD [ "python", "subtitles_translator/cli.py"]
