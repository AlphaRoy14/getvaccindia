#! /usr/bin/env bash

set -e

pyclean .
celery beat -A scheduler --loglevel=INFO --pidfile=/opt/celeryd.pid