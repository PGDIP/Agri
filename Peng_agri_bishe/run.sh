#!/bin/bash
mongod -dbpath=/usr/local/mongodb/data -logpath=/usr/local/mongodb/logs --fork
nohup python manage.py runserver 0.0.0.0:8000 &