# ---------------------------------- WARNING ----------------------------------
# This file is primarily for production use with k8s
# See Dockerfile in subdirectories for dev use with docker-compose
# ---------------------------------- WARNING ----------------------------------

# ---
# build scss in separate image
# ---
FROM node:26-alpine as sass-compile

WORKDIR /app

COPY ./sass-compile/package.json ./sass-compile/package-lock.json ./
RUN npm ci

COPY ./sass-compile/scss ./scss

RUN npm run css

# ---
# wagtail image
# ---
# Use an official Python runtime based on Debian 12 "trixie" as a parent image.
FROM python:3.14-slim-trixie AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Add user that will be used in the container.
RUN useradd wagtail

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*


# Install the project requirements.
ENV UV_COMPILE_BYTECODE=1 \
	UV_LINK_MODE=copy \
	UV_PYTHON_DOWNLOADS=0 \
	UV_PROJECT_ENVIRONMENT=/opt/venv \
	PATH="/opt/venv/bin:$PATH"

COPY stanovanja/pyproject.toml stanovanja/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --locked --no-dev --no-install-project

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail ./obljubadeladolg .

RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --locked --no-dev

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

# Copy compiled css from other image
COPY --chown=wagtail:wagtail --from=sass-compile /app/static/css ./obljubadeladolg/static/css


FROM python:3.14-slim-trixie AS runtime

# Add user that will be used in the container.
RUN useradd wagtail

EXPOSE 8000

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
	PATH="/opt/venv/bin:$PATH" \
	PYTHONUNBUFFERED=1 \
    PORT=8000

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

USER wagtail

CMD gunicorn obljubadeladolg.wsgi:application -b 0.0.0.0:8000 --log-level DEBUG
