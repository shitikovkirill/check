# cecks

## Run

```bash
docker compose up
```

Go to [local dev](http://127.0.0.1:8000)

## Run tests

```bash
docker compose run api test
```

## Show coverage

```bash
python -m http.server 8000 --directory htmlcov/ --bind 0.0.0.0
```
