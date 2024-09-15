#!/bin/bash

# Update system to latest
sudo apt update && sudo apt upgrade -y

# Install libcamera, virtualenv and git
sudo apt install -y libcamera-apps python3-venv git

# Clone the project
# git clone git@github.com:thomas/racecar.git
# cd racecar

# Create a Virtual Environment
python3 -m venv venv

# Activate the Virtual Environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install necessary packages
pip install -r requirements.txt

echo "Setup complete. You can now run the app using 'python app.py'."