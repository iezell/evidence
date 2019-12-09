#!/bin/bash

echo Running Object Test
exec python3 manage.py makemigrations
exec python3 manage.py migrate
exec python3 manage.py test
