#!/bin/bash

mv /SIMPLE/ /root/
cd ..
sudo rm -rf cyberdeck

cd /root/SIMPLE/

echo "Updating and upgrading system..."
apt-get update && apt-get upgrade -y

echo "downloading python"
apt-get install -y python3 python3-pip python3-venv git

echo "installing packages"
pip3 install -r requirements.txt



#REUSABLE SERVICE MAKER SO I DONT HAVE TO FIND THAT FORUM EVERYTIME
SERVICE_NAME="main"
EXECUTABLE_PATH="/root/SIMPLE/main.py"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

echo "[Unit]
Description=$SERVICE_NAME
After=network.target

[Service]
Type=simple
User=root
ExecStart=$EXECUTABLE_PATH
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target" | sudo tee "$SERVICE_FILE" > /dev/null

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"

echo "Service status:"
sudo systemctl status "$SERVICE_NAME" --no-pager
#END OF REUSABLE SERVICE SCRIPT