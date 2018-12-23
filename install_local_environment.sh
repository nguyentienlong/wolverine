#!/usr/bin/env bash
echo "Install required packages"

case `uname` in
    Linux )
        sudo apt-get update
        sudo apt-get install build-essential python-pip libffi-dev python-dev python3-dev libpq-dev
        sudo sudo apt-get install -y mongodb
        sudo systemctl status mongodb
        ;;
    Darwin )
        brew update
        brew install mongodb

        COUNT=`ps aux | grep mongod | wc -l`
        if [ "$COUNT" -lt 2 ]; then
            echo "start mongo db"
            mongod --config conf/mongod.conf  &
        fi
        ;;
    *)
    exit 1
    ;;
esac

sudo pip install virtualenv

type virtualenv >/dev/null 2>&1 || { echo >&2 "No suitable python virtual env tool found, aborting"; exit 1; }

#rm -rf .venv
virtualenv -p python3 .venv
source .venv/bin/activate
pip3 install -r requirements.txt

## todo
## copy conf file to app.ini
## if pwd contains stag, copy stag file
## if pwd contains stag, copy prod file
