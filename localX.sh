#!/usr/bin/env bash
echo "copy local configuration"
cp conf/local.ini conf/app.ini
cp conf/firebase_adminsdk_credentials.json.local conf/firebase_adminsdk_credentials.json

echo "start local web app"
PORT=30000
lsof -i | grep $PORT | awk '{print $2}' | xargs -I$ kill -9 $

gunicorn app.main:application -b :$PORT --reload &

