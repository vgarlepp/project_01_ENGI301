# Project 1, ENGI 301, Vanessa Garlepp
This project is the development code for an LED-based maze game. An accelerometer will detect movement, and compare this movement to thresholds to determine in which direction the pixel will move. This repository contains preliminary codes which use a random number generator to move the pixel throughout the maze in a series of images. This code can later be easily adapted to take in data from the accelerometer and output movement to the LED matrix. 

In order to run the code, connect your Pocketbeagle to your desktop, ensure it is connected to the network, and open the Cloud9 IDE. Open all 3 scripts included in the "code" folder. Ensure that you have the following python version 3+ installed, and run the following commands:

sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-smbus -y
sudo apt-get install python-pip python3-pip -y
sudo apt-get install zip
sudo pip3 install --upgrade setuptools
sudo pip3 install --upgrade Adafruit_BBIO
sudo pip3 install adafruit-blinka

In addition, install the following python libraries/functionalities for this project (import code is included in the python scripts):

Pillow (PIL)
colorsys
time
numpy
io
board
random
math
adafruit_mpu6050

Then run this command:

sudo python3 maze_game.py

Type in the sudo password, and run. A series of .tmp images will appear in the folder in which the scripts are saved, as the random number generator pushes the pixel through the maze. Click control + C to stop the algorithm, or allow it to run until the pixel reaches the finish point, in which case the script will stop running automatically. Click through the images to see the pixel's movement randomly through the maze.

The future intention for these scripts is to integrate into the aforementioned maze prototype. The final edits include taking input from the accelerometer, and pushing the movement outputs to the LED board each time to move the pixel. 
