#!/bin/bash
uvicorn config.asgi:fastapi_app --reload --host 0.0.0.0 --port 8000 &
uvicorn config.asgi:django_app --reload --host 0.0.0.0 --port 8001
