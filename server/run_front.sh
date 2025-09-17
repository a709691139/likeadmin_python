#!/usr/bin/env bash

# 运行服务
python3 -m uvicorn asgi_front:app --port 8002 --reload --host 0.0.0.0
