#!/bin/bash

GIT_DIR=/opt/git
IFACEFAILOVER_DIR=/opt/ifacefailover

# Install the python package manager and developer tools
sudo apt-get install python-pip python-dev build-essential

# http://docs.python-requests.org/en/latest/
sudo pip install requests

# https://pypi.python.org/pypi/pynetinfo
sudo mkdir -p $GIT_DIR/pynetinfo
sudo git clone https://github.com/ico2/pynetinfo $GIT_DIR/pynetinfo
cd $GIT_DIR/pynetinfo
sudo python setup.py install

# https://github.com/shellbit/ifacefailover/wiki
# Create the ifacefailover directory structure and link to the GIT src
sudo mkdir -p $IFACEFAILOVER_DIR/{config,logs}
sudo ln -s $GIT_DIR/ifacefailover/src $IFACEFAILOVER_DIR/src

# Serialize the default route handlers and verifiers
sudo python -m compileall $IFACEFAILOVER_DIR/src
sudo PYTHONPATH="$PYTHONPATH:$IFACEFAILOVER_DIR/src" python $GIT_DIR/ifacefailover/pkl.py $IFACEFAILOVER_DIR/config

# Copy the default log configuration from src
sudo cp $GIT_DIR/ifacefailover/log.properties $IFACEFAILOVER_DIR/config

# Copy the default ifacefailover property configuration
sudo cp $GIT_DIR/ifacefailover/ifacefailover.properties.sample $IFACEFAILOVER_DIR/config/ifacefailover.properties

# Copy the startup service
sudo cp $GIT_DIR/ifacefailover/ifacefailover /etc/init.d
sudo chmod 755 /etc/init.d/ifacefailover
sudo update-rc.d ifacefailover defaults 100