#!/bin/sh

gunicorn -w 2 -b 0.0.0.0:8000 main:app --log-file /dev/stderr --access-logfile /dev/stdout
