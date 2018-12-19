#!/bin/bash
echo "start running"
pwd
nohup python3 /opt/app-root/src/run.py &
nohup python3 /opt/app-root/src/core.py &
tail -f requirements.txt
