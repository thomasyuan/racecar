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
  - `sudo apt install python3-smbus i2c-tools`

## Run the app

## Install opencv-python

Seems either pi zero doesn't have enough power, or there is a bug (even pi 3 seems stuck as well). When install opencv-python, it will stuck on building. Some one figured that install with version number seems can fix the building stuck issue.
`pip install opencv-python==4.10.0.84`

Need install `sudo apt install pypy3-dev`

> https://github.com/opencv/opencv-python/issues/391

## Shell do everything.

`setup.sh`


{
    "command": "turn_right",
    "degree": 90
}