#! /usr/bin/env bash

set -e

pyclean .
uvicorn main:app --host 0.0.0.0 --port 80