#!/bin/bash
set -e

until pg_isready --host=$POSTGRES_HOST --port=5432 --dbname=$POSTGRES_DB --username=$POSTGRES_USER
do
    echo "Aguardando PostgresSQL"
    sleep 3;
done
echo "PosgresSQL está pronto para receber conexão!"

python /app/source/manage.py migrate
python /app/source/manage.py seed --create-superuser
python /app/source/manage.py runserver 0.0.0.0:8000

