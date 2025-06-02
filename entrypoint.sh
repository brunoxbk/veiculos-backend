#!/bin/sh


echo "Waiting for postgres..."

while ! nc -z db $DB_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate --noinput
echo "run migrations"

if [ "$DEBUG" = "False" ]
then
  python manage.py collectstatic --noinput
  echo "colleted static files"

  exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
else
  exec python manage.py runserver 0.0.0.0:8000
fi