#!/bin/sh

set -e

prod() {
    echo "Starting application..."

    poetry install

    exec poetry run start
}

migrate() {
    echo "Run migration..."

    wait-for-it db:5432

    alembic -c alembic.ini upgrade head
}

dev() {
    echo "Dev..."
    createkey

    migrate

    prod
}

createkey() {
    echo "Create key..."
    mkdir -p ./tmp

    FILE=./tmp/private.pem

    if [ -f $FILE ]; then
        echo "File $FILE exists."
    else
        echo "File $FILE does not exist."
        ssh-keygen -t rsa -b 4096 -m PEM -f ./tmp/private.pem -q -N ""
        ssh-keygen -f ./tmp/private.pem -e -m PKCS8 > ./tmp/public.pem
    fi
}

debug() {
    echo "Debug..."

    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app/ --dev
}

test() {
    echo "Runn tests..."

    createkey

    migrate

    exec pytest ./tests  --no-cov-on-fail

    exec python -m http.server 8000 --directory htmlcov/ --bind 0.0.0.0
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
