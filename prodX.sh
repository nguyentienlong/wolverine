#!/usr/bin/env bash
echo "copy prod configuration"
cp conf/prod.ini conf/app.ini
cp conf/firebase_adminsdk_credentials.json.prod conf/firebase_adminsdk_credentials.json

echo "update code ..."
git reset --hard
git pull origin master -f

echo "restarting prod web app ..."
PORT=50000
ps aux | grep $PORT | awk '{print $2}' | xargs -I$ kill $
sleep 5

LOG_DIR=/tmp/vietvivu365/api/
LOG_FILE=/tmp/vietvivu365/api/prod.log
if [ -f "$LOG_DIR" ]
then
	echo "$LOG_DIR found."
else
    mkdir -p $LOG_DIR
fi

gunicorn app.main:application -b :$PORT --reload &

echo "prod api ready ^^"

# TODO: copy nginx conf, then restart nginx
