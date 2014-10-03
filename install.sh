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
sudo python $IFACEFAILOVER_DIR/pynetinfo/setup.py install

# https://github.com/shellbit/ifacefailover/wiki
# Create the ifacefailover directory structure and link to the GIT src
sudo mkdir -p $IFACEFAILOVER_DIR/{config,logs}
sudo ln -s $IFACEFAILOVER_DIR/src $GIT_DIR/ifacefailover/src

# Serialize the default route handlers and verifiers
sudo python $IFACEFAILOVER_DIR/src/pkl.py $IFACEFAILOVER_DIR/config

# Copy the default log configuration from src
sudo cp $IFACEFAILOVER_DIR/src/log.properties $IFACEFAILOVER_DIR/config

# Copy the default ifacefailover property configuration
sudo cp $IFACEFAILOVER_DIR/src/ifacefailover.properties.sample $IFACEFAILOVER_DIR/config/ifacefailover.properties

# Copy the startup service
sudo cp $IFACEFAILOVER_DIR/src/ifacefailover /etc/init.d