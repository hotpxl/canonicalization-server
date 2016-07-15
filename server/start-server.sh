#!/bin/bash
set -euo pipefail
gunicorn -c gunicorn_config.py server:app --access-logfile='-'
