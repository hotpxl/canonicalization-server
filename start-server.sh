#!/bin/bash
gunicorn -c gunicorn_config.py server:app --access-logfile='-'
