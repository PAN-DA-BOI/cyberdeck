#!/bin/bash

# Update and upgrade system
echo "Updating and upgrading system..."
apt-get update && apt-get upgrade -y

# Install Python and pip
echo "Installing Python and pip..."
apt-get install -y python3 python3-pip python3-venv git

# Install required Python packages
echo "Installing Python packages..."
pip3 install --upgrade pip
pip3 install -r requirements.txt  # Assumes you have a requirements.txt in your project

# Install X11 window manager (Openbox)
echo "Installing X11 window manager (Openbox)..."
apt-get install -y openbox xinit xserver-xorg x11-xserver-utils

# Create a minimal ~/.xinitrc to start your Python GUI
echo "Configuring ~/.xinitrc..."
cat > /home/$SUDO_USER/.xinitrc << 'EOL'
#!/bin/bash
# Rotate screen 180 degrees
xrandr --output $(xrandr | grep " connected" | cut -d" " -f1) --rotate inverted

# Start your Python GUI
cd /home/$USER
python3 main.py
EOL
chown $SUDO_USER:$SUDO_USER /home/$SUDO_USER/.xinitrc
chmod +x /home/$SUDO_USER/.xinitrc

# Create a systemd service to start X and your GUI on boot
echo "Creating systemd service..."
cat > /etc/systemd/system/gui.service << 'EOL'
[Unit]
Description=Start X and Python GUI
After=multi-user.target

[Service]
Type=simple
User=$SUDO_USER
ExecStart=/bin/bash -c 'startx /etc/X11/xinit/xinitrc -- :0 vt1'
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOL

# Enable the service to start on boot
systemctl enable gui.service

# Disable other display managers (like GDM, LightDM)
echo "Disabling other display managers..."
systemctl disable gdm3 lightdm

# Set Openbox as the default window manager
echo "Setting Openbox as default window manager..."
update-alternatives --set x-window-manager /usr/bin/openbox

# Reboot to apply changes
echo "Setup complete. Rebooting in 5 seconds..."
sleep 5
reboot
