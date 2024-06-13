ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

RUN apt update && apt upgrade -y && apt install jq nginx supervisor \
                              --no-install-recommends -y && apt-get clean
RUN pip install --progress-bar off -U wheel setuptools && rm -rf ~/.cache/pip/*
RUN rm /etc/nginx/sites-enabled/default

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    jobFinder

RUN chown -R jobFinder:jobFinder /var/log/nginx
RUN chown -R jobFinder:jobFinder /var/lib/nginx/
RUN mkdir -p /opt/supervisord
RUN chown -R jobFinder:jobFinder /opt/supervisord

# Copy the source code into the container.
COPY . .

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER jobFinder

# Expose the port that the application listens on.
EXPOSE 8000

COPY nginx/nginx.conf /etc/nginx/
COPY nginx/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY nginx/supervisord.conf /etc/

ENV LOG_LEVEL=INFO

# Run the application.
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]