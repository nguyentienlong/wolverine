#!/usr/bin/env bash
echo "copy stag configuration"
cp conf/stag.ini conf/app.ini
cp conf/firebase_adminsdk_credentials.json.stag conf/firebase_adminsdk_credentials.json

echo "update code ..."
git reset --hard
git pull origin master -f

echo "restarting stag web app ..."
PORT=40000
ps aux | grep $PORT | awk '{print $2}' | xargs -I$ kill $
sleep 5

LOG_DIR=/tmp/vietvivu365/api/
LOG_FILE=/tmp/vietvivu365/api/stag.log
if [ -f "$LOG_DIR" ]
then
	echo "$LOG_DIR found."
else
    mkdir -p $LOG_DIR
fi

gunicorn app.main:application -b :$PORT --reload &

echo "stag api ready!"

# TODO: copy nginx conf, then restart nginx
