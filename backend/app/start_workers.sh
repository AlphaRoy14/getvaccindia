#! /usr/bin/env bash

set -e

pyclean .
celery worker -A worker -A scheduler -l INFO -c 3 --pidfile=/opt/celeryd.pid
# celery worker -A scheduler -l INFO -c 1 --pidfile=/opt/celeryd.pid