#!/bin/bash
source venv/bin/activate
pip install -r requirements.txt
exec gunicorn app:app \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --access-logfile '-' \
    --error-logfile '-'

