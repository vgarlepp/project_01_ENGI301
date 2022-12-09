"""
This script reads the current position and displays this change on the LED board.

**For rough draft**: prints matrix instead of displaying on LED board. 
Updates as the random number generator moves the pixel through the maze.
"""

# ------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------

# imports to communicate with the board
from PIL import Image, ImageFont, ImageDraw
import time, datetime
from colorsys import hsv_to_rgb 
import io
# import pyledscape
import numpy as np

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

X = 0
Y = 1

# initializing variables for the matrix
i = 0
WIDTH = 64
HEIGHT = 64

WALL_COLOR       = (0x00, 0x00, 0x00) # black
BACKGROUND_COLOR = (0xFF, 0xFF, 0xFF) # white
POS_COLOR        = (0xFF, 0x00, 0x00) # red
WINNING_COLOR    = (0x00, 0x00, 0xFF) # blue

# base maze array
base_maze = [
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

# make sure the base_maze is 64 x 64
# base_maze = np.reshape(base_maze, (64, 64))
        
# ------------------------------------------------------------------------
# Functions 
# ------------------------------------------------------------------------

class Maze_Display():
    
    # class variables:
    maze = None
    curr_pos = None
    winning_pos = None
    im = None
    matrix = None
    
    def __init__(self, maze, starting_pos, winning_pos):
        """Initializes everything needed for the class"""
        
        # initialize class variables
        self.maze        = maze
        self.curr_pos    = starting_pos
        self.winning_pos = winning_pos
        
        # allocates memory array to fill with pixel values
        # self.im = Image.new("RGBX", (WIDTH,HEIGHT), "black")
        self.im = Image.new("RGB", (WIDTH,HEIGHT), "white")
        self.create_maze()
        
        # Not in use:
        # im_draw = ImageDraw.Draw(im) # used by Pillow to interact with drawing

        # initialize function for matrix itself (used when LED board is connected)
        # self.matrix = pyledscape.pyLEDscape()
        
    # End def
    
    def create_maze(self):
        """Create maze from the base_maze array"""
        # create array of pixel values from black image
        pixels = self.im.load()
        
        for i in range(self.im.size[0]):
            for j in range(self.im.size[1]):
                if self.maze[j][i] == 1:
                    # pixels[i,j] = (0xff, 0xff, 0xff) # color = white
                    pixels[i,j] = WALL_COLOR # color = black
                    # the rest of the pixels stay black

        pixels[self.winning_pos[X], self.winning_pos[Y]] = WINNING_COLOR
        
        self.im.save("tmp_01.png")
        
    # End def

    def update_pos(self, pos):
        """Updates the position of the dot within the maze  
        This function will return a new maze output with the new position"""
        
        # create array of pixel values from black image
        pixels = self.im.load()
        
        # convert old pixel location to background color
        pixels[self.curr_pos[X], self.curr_pos[Y]] = BACKGROUND_COLOR

        # set this position up to be reset in the next loop
        self.curr_pos = pos

        # establishes the new pixel location as the position color
        pixels[self.curr_pos[X], self.curr_pos[Y]] = POS_COLOR

        self.im.save("tmp_{0}.png".format(time.time()))
        
        # update the display
        # •••••• This would contain the production code to the LED matrix
        
    # End def
    
    def print_maze(self):
        """Prints a maze using spaces and vertical lines.Prints
        
        Will be modified to change (x,y) of curr_pos to another number that gets read into the image as a different color,
        then convert to an image which gets pushed to the board"""
        
        # puts a new line between repeated maze prints
        output = "MAZE:\n"
        
        for y,line in enumerate(self.maze):
            for x,val in enumerate(line):

                # indicate current position with a star
                if (x,y) == self.curr_pos:
                    output += "*"
                    
                # indicate winning position with an @ sign
                elif (x,y) == self.winning_pos:
                    output += "@"
               
                # replace 0,'s with spaces and 1,'s with vertical lines
                else:
                    if val == 0:
                        output += " "
                    else:
                        output += "|"
            
            # create a new line            
            output += "\n"
            
        print(output)
        
    # End def
    
# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

# main function script, serves as testing when maze_game.py is run
if __name__ == "__main__":
    
    # instantiate maze class for maze display (create maze display)
    display = Maze_Display(base_maze, (1,1), (62,62))
    
    # call function
    display.update_pos((7,1))
    
# End def