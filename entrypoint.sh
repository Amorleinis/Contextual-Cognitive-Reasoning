#!/bin/bash
# Entrypoint for Contextual Reasoning AI container
# Usage: ./entrypoint.sh [api|cli|gui] [arguments]

MODE=$1
shift || true

case "$MODE" in
  api)
    echo "Starting FastAPI server..."
    uvicorn contextual_reasoning_ai.api.server:app --host 0.0.0.0 --port 8000
    ;;
  cli)
    echo "Running CLI mode..."
    python main_cli.py "$@"
    ;;
  gui)
    echo "Starting GUI mode..."
    python main_gui.py
    ;;
  *)
    echo "Usage: $0 [api|cli|gui] [arguments]"
    exit 1
    ;;
esac
