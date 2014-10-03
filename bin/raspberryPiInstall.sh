#!/bin/bash

# Consider performing a system update and upgrade
#sudo apt-get update
#sudo apt-get upgrade

# Disable the kernel's use of the hardware serial connection
sudo wget https://raw.github.com/lurch/rpi-serial-console/master/rpi-serial-console -O /usr/bin/rpi-serial-console && sudo chmod +x /usr/bin/rpi-serial-console
sudo rpi-serial-console disable
echo "Use of the kernel's hardware serial connection has been disabled. You will need to reboot."

# Install the point-to-point protocol daemon
sudo apt-get install ppp screen elinks

# Download the Fona peer
FONA_PEER=/etc/ppp/peers/fona
wget https://raw.githubusercontent.com/adafruit/FONA_PPP/master/fona -O $FONA_PEER
echo "FONA peer has been installed at $FONA_PEER"
echo "You need to update this file with an APN and serial port"