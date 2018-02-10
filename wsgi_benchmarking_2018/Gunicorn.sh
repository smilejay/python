#!/bin/bash
set -x
PROCESSOR_COUNT=$(nproc)
# This formula is recommended in the Gunicorn documentation
# http://docs.gunicorn.org/en/stable/design.html#how-many-workers
GUNICORN_WORKER_COUNT=$(( PROCESSOR_COUNT * 2 + 1 ))

gunicorn -w ${GUNICORN_WORKER_COUNT} -b 0.0.0.0:8200 app:application
