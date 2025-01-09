#!/bin/sh

set -e

prod() {
    echo "Starting application..."

    poetry install

    exec poetry run start
}

migrate() {
    echo "Run migration..."

    # alembic -c alembic.ini upgrade head
}

dev() {
    echo "Dev..."

    migrate

    prod
}

debug() {
    echo "Debug..."

    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app/ --dev
}

test() {
    echo "Runn tests..."

    exec pytest ./tests --cov=tournaments.api --cov-report=html
}

help() {
    echo "Help"
}

case $1 in
prod|dev|debug|test|help)
    $1 ${@:2}
    ;;
*)
    exec $1 ${@:2}
    ;;
esac
