## MEC 2024 Robotic Car Race

## Raspberry pi zero setup.

- Flash latest build using Raspberry Pi Imager
- Update system to latest
- Install libcamera tools
  - `sudo apt install libcamera-apps`
  - Try it `libcamera-still -o test.jpg` to check if camera is ready
- Setup python evn
  - install virtualenv: `sudo apt install python3-venv`
  - Create a Virtual Environment: go to project folder and run `python3 -m venv venv`
  - Activate the Virtual Environment: `source venv/bin/activate`
  - upgrade pip `pip install --upgrade pip`
  - Install Requirements: `pip install -r requirements.txt`

## Run the app

## Shell do everything.

```code=bash
#!/bin/bash

# Update system to latest
sudo apt update && sudo apt upgrade -y

# Install libcamera, virtualenv and git
sudo apt install -y libcamera-apps python3-venv git

# Clone the project
git clone git@github.com:thomas/racecar.git
cd racecar

# Create a Virtual Environment
python3 -m venv venv

# Activate the Virtual Environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install necessary packages
pip install -r requirements.txt

echo "Setup complete. You can now run the app using 'python app.py'."
```
