#!/bin/bash
sudo service ifacefailover stop
sudo python /home/pi/fonapwr.py
sudo poff fona
sudo service ifacefailover start
