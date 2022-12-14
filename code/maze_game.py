"""
This is the main script. 

Tasks:
- Define base maze structure and display on the LED board
- Take direction input from sensor.py
- Update dot position on board based on direction input
- Indicate when the dot has reached the winning position
- Clear the board when starting over

"""

# ------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------

import time
import board
import Adafruit_BBIO.GPIO as GPIO
import display as maze_display
import sensor as maze_sensor

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

X = 0
Y = 1

# static maze structure
BASE_MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,0,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,1,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,1,1,1,0,1,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1,0,1,0,0,0,0,1,1,1,0,1,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,0,0,0,0,1,0,1,1,0,0,0,0,0,1,1,1,0,1,0,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,0,0,0,1,0,1,1,1,1,0,0,0,0,0,1,0,1,1,0,1,0,1],
    [1,0,0,0,1,0,1,1,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,0,0,0,1,1,1,1,1,0,0,0,0,1,0,1],
    [1,1,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,1,1,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,0,0,0,0,1,0,1,1,1,1,0,0,1,0,1,1,1,0,1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,1,1],
    [1,0,1,0,0,0,0,0,1,0,1,1,1,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,1,1,1,1,1,0,1,1,0,0,1,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,0,0,1,0,0,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,1],
    [1,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,0,0,1,0,0,0,0,0,1,1,1,1,1,1,0,1,1,0,0,0,0,0,1],
    [1,1,1,1,1,0,1,0,1,0,0,0,0,1,1,1,1,1,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1,0,1,0,1,0,1,0,0,0,0,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,0,1,0,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,1,1,1,0,1,0,1,1,1,1,0,0,1,0,1,1,1,1,1,1,0,1,1,1,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,1,0,0,1],
    [1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1,1,1,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1,1],
    [1,0,1,0,1,0,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,1,1,0,0,0,0,0,0,1,0,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,0,1],
    [1,0,1,1,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,1,1,1,0,0,1,0,1,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,1,0,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,0,0,1,0,1,1,1,1,0,1,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,0,0,0,0,0,1,1,0,0,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1],
    [1,0,1,0,0,0,0,1,0,1,1,1,1,0,1,1,1,0,1,0,1,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,1],
    [1,0,1,0,1,1,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,0,1,1,1,1,1,0,1,1,1,1,0,0,0,1,0,0,1],
    [1,0,0,0,0,1,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,1],
    [1,1,1,1,1,1,0,1,0,0,0,0,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,0,1,0,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1,1,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,1,0,0,0,1,1,1,1,1],
    [1,1,1,1,0,1,1,1,0,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,1,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,1,1,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,0,1,0,1,1,0,1,0,1,0,1,1,1,0,1,0,0,0,1,0,1,1,1,1,0,1,0,1,1,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,1],
    [1,0,1,0,1,0,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,0,0,1,1,1,1,0,1],
    [1,0,1,0,1,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,0,0,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,1,1,1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,1,1,1,0,1,0,1,0,0,0,1,0,1,1,1,1,0,1,0,0,0,1,0,1,0,1,1,0,1,0,0,0,0,1,1,1,1,1,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,1,1,1,1,0,1,1,1,0,0,0,0,1,0,1,1,1,0,0,0,0,0,0,1,0,1,0,1,1,1,1,1,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,1,1,1,0,1,0,1,0,0,0,0,0,1,1,1,0,1,1,0,0,1,1,1,0,1,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,0,0,0,0,1,0,1,0,0,0,1,1,1,0,1,0,1,0,0,0,0,1,1,0,1,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1,0,1,1,1,0,1,0,1,0,0,0,1,0,1,1,1,1,0,0,1,0,1,1,1,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1],
    [1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1],
    [1,0,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1],
    [1,0,0,0,0,0,1,1,1,0,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1],
    [1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,1,1,1,0,1,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,1,1,1,0,1,1,1,1,1,0,0,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1],
    [1,1,1,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,1,0,1,0,1,0,0,1,0,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,1,0,1,0,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,0,1,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1],
    [1,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,0,1],
    [1,0,0,1,0,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,0,0,0,0,1,0,0,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,0,1,1,1,1,1],
    [1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,1],
    [1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1,1,1],
    [1,0,0,0,0,1,0,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,0,0,0,1,0,0,0,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,0,1,0,1,1,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,0,1,0,0,0,0,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,0,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,0,1,0,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1,1,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,0,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    
# Delay time between maze updates
DELAY = 0.5

# Established start/winning positions    
STARTING_POS = (1,1)
WINNING_POS = (62,62)

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

class Maze_Game():
    
    # class variables:
    maze     = None             # Data structure representing the base maze
    display  = None             # Display for the maze
    sensor   = None             # Sensor to move the cursor
    curr_pos = None             # Current position of the player in the maze; tuple (x, y)
    win_pos  = None             # Winning position of the maze
    switch   = None             # Switch to start / reset the game
    
    x_thres = None             # Sensor X Threshold
    y_thres = None             # Sensor Y Threshold
    i2c      = None             # Sensor I2C bus
    
    def __init__(self, maze, starting_pos=STARTING_POS, winning_pos=WINNING_POS, 
                       switch="P2_1", i2c=board.I2C()):
        """Initialize class variables"""
        self.maze     = maze
        self.curr_pos = starting_pos       # When maze is instantiated, current position is starting position 
        self.win_pos  = winning_pos     
        self.switch   = switch
        
        self.x_thres = 5                  # NEEDS TO BE TESTED AND ADJUSTED
        self.y_thres = 5                  # NEEDS TO BE TESTED AND ADJUSTED
        self.i2c      = i2c

        self.debug    = True
        
        # Set up the hardware
        self._setup()
        
    # End def
        
    def _setup(self):
        """Set up the LED and sensors"""
        
        # Initialize display
        self.display = maze_display.Maze_Display(self.maze, self.curr_pos, self.win_pos)
        
        # Initialize sensors
        self.sensor  = maze_sensor.Maze_Sensor(self.x_thres, self.y_thres, self.i2c)
        
        # Initialize switch
        GPIO.setup(self.switch, GPIO.IN)
        
    # End def
    
    
    def update_pos(self):
        """Updates the dot's position based on the sensor output"""
        
        # Get direction of the move from the sensor
        (x_dir, y_dir) = self.sensor.get_direction()
        
        # Debug option
        if self.debug:
            print("X = {0}, Y = {1}".format(x_dir, y_dir))
        
        # Update position based on sensor direction
        if y_dir == maze_sensor.UP:
            # checks if the upwards index is 0 (open for moving)
            if self.maze[self.curr_pos[Y]-1][self.curr_pos[X]] == 0:
                # updates current position to move upwards
                self.curr_pos = (self.curr_pos[X], self.curr_pos[Y]-1)
        
        if y_dir == maze_sensor.DOWN:
            if self.maze[self.curr_pos[Y]+1][self.curr_pos[X]] == 0:
                self.curr_pos = (self.curr_pos[X], self.curr_pos[y]+1)
                
        if x_dir == maze_sensor.LEFT:
            if self.maze[self.curr_pos[Y]][self.curr_pos[X]-1] == 0:
                self.curr_pos = (self.curr_pos[X]-1, self.curr_pos[Y])
        
        if x_dir == maze_sensor.RIGHT:
            if self.maze[self.curr_pos[Y]][self.curr_pos[X]+1] == 0:
                self.curr_pos = (self.curr_pos[X]+1, self.curr_pos[Y])
    
    # End def
    
    
    def check_winning_pos(self, curr_pos):
        """Compares current position to winning position and returns the value if it wins"""
        ret_val = False
        
        if self.curr_pos[X] != self.win_pos[X]:
            ret_val = True
        
        if self.curr_pos[Y] != self.win_pos[Y]:
            ret_val = True
        
        return ret_val
        
    # End def
    
    def wait_for_start(self):
        """Takes switch input to start the game"""
        
        if self.debug: 
            print("Waiting to start game")
        
        # REAL CODE
        # Wait for button to be pressed
#        while(GPIO.input(self.switch) == 1):
#            time.sleep(0.1)
            
        # Wait for button to be released
#        while(GPIO.input(self.switch) == 0):
#            time.sleep(0.1)

        # TEST CODE
        time.sleep(5)
        
        if self.debug:
            print("Starting game")
            
    # End def
    
    
    def run(self):
        """Runs the script, cycles in delay time"""
        
        # Update display
        self.display.update_pos(self.curr_pos)
        
        # Loop to play multiple games in a row
        while True:
            
            # Wait for the start
            self.wait_for_start()
        
            # Loop for a single game
            while True:
                
                # Update position based on sensor output
                self.update_pos()
                
                # Update display w new position
                self.display.update_pos(self.curr_pos)
                
                # Check if the dot is in the winning position
                ret_val = self.check_winning_pos(self.curr_pos)
                
                # If the player won, exit the game and clean up
                if (ret_val == False):
                    print("You win!")
                    break
                
                # Wait to update display
                time.sleep(DELAY)
                
            # Wait for switch press to start over
            self.wait_for_start()
            
            # Clean up to start over
            self.cleanup()
        
    # End def
    
    def cleanup(self):
        """ Cleans up the maze when restarting"""
        
        # set position back to starting position
        self.curr_pos = STARTING_POS
        
        # Update display
        self.display.update_pos(self.curr_pos)
        
    # End def
    
# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
    
if __name__ == "__main__":
    """Main script that runs the entire maze_game program"""
    
    # instantiate maze game
    maze_game = Maze_Game(BASE_MAZE)
    
    # Run maze game
    try: 
        maze_game.run()
        
    except KeyboardInterrupt:
        print("Maze game ended. Resetting")
        maze_game.cleanup()
        
    print("Game over")
    
# End def