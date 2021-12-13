#!/bin/sh
export PYTHONPATH=/opt/cloud_api/source/

if [ "$FLASK_DEV_ENV" = "true" ];
then
  export FLASK_APP=source.main:app
  export FLASK_ENV=development
  flask run --host=0.0.0.0 --port 5000
else
  gunicorn -b  0.0.0.0:5000 $@ \
    --log-level=INFO \
    --access-logfile - \
    -w $(( 2 * `cat /proc/cpuinfo | grep 'core id' | wc -l` + 1 )) \
    --max-requests 1000 \
    -k gevent \
    source.main:app
fi