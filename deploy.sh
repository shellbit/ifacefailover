#!/bin/bash
SERVICE_NAME=ifacefailover
LOCAL_DIR=/home/akohring/git/ifacefailover
REMOTE_SERVER=pi@piphone
REMOTE_DIR=/opt/ifacefailover
COMMAND=$REMOTE_SERVER:$REMOTE_DIR

ssh -t $REMOTE_SERVER "sudo service $SERVICE_NAME stop"
rsync -avz --delete --exclude *.pyc -e ssh $LOCAL_DIR/src $COMMAND
rsync -avz -e ssh $LOCAL_DIR/pkl.py $COMMAND/config
ssh -t $REMOTE_SERVER "rm -f $REMOTE_DIR/src/*.pyc; python -m compileall $REMOTE_DIR"
ssh -t $REMOTE_SERVER "export PYTHONPATH="$PYTHONPATH:$REMOTE_DIR/src"; python $REMOTE_DIR/config/pkl.py"
ssh -f $REMOTE_SERVER "sudo service $SERVICE_NAME start; sudo service $SERVICE_NAME status"
