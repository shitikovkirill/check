import argparse

import uvicorn
from fastapi import FastAPI

from app.routes import auth, check, template

app = FastAPI(title="App")


routes = [
    {"router": auth.router, "prefix": "/api"},
    {"router": check.router, "prefix": "/api"},
    {"router": template.router, "prefix": "/template"},
]

for rout in routes:
    app.include_router(**rout)


def start():
    """Launched with `poetry run start` at root level"""
    parser = argparse.ArgumentParser(description="Start app.")
    parser.add_argument("--dev", action="store_true", help="Set reload arg.")
    args = parser.parse_args()

    uvicorn.run(
        "app.__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=args.dev,
    )


if __name__ == "__main__":
    start()
