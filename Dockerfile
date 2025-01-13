FROM debian:bookworm AS download-migrate
RUN apt-get update && apt-get install -y curl
RUN curl -Ls https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o wait-for-it.sh && \
    chmod +x wait-for-it.sh

FROM python:3.12-alpine as dev

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

RUN apk add gcc \
            curl \
            openssh-keygen \
            bash \
            musl-dev --no-cache && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apk del curl

COPY --from=download-migrate /wait-for-it.sh /usr/bin/wait-for-it
COPY [".", "."]

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction \
                   --no-ansi \
                   -vvv

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
