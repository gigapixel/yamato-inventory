#!/bin/bash

source /etc/profile.d/python.sh

echo "Begining script sync Stock pcms on $(date)" >> /data/logs/ems/pcms_sys_stock.log

python /data/projects/ems/pcms_stock_sync/pcms_stock.py

echo "finish script sync Stock pcms on $(date)" >> /data/logs/ems/pcms_sys_stock.log
