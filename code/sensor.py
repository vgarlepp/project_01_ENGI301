"""
This script reads outputs from the MPU 6050 and determines a direction the dot should move.
"""

# ------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------

# MPU interface files

# download adafruit MPU6050

import time
import random
import math
import board
import adafruit_mpu6050

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"
NONE = "none"

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

class Maze_Sensor():
    
    # class variables:
    thres_x = None
    thres_y = None
    mpu = None
    
    # initialize class variables
    def __init__(self, thres_x, thres_y, i2c=board.I2C()):
        self.thres_x = thres_x
        self.thres_y = thres_y
#         self.mpu = adafruit_mpu6050.MPU6050(i2c) # ONLY HOOK THIS UP TO i2c1
        
        # sort/label values
        
    # End def
    
    
    def get_imu_value(self):
        """Obtains the necessary values from the sensor and assigns them to 
        class variables"""
        
        # FINAL CODE: 
        # grab values from MPU 6050 and assign to class variables pos_x and pos_y
#        pos_x = self.mpu.acceleration[1]
#        pos_y = self.mpu.acceleration[2]
        
        # Test code:
        pos_x = random.random() * 10 # uniformly distributed random number between 0 and 10
        pos_x = pos_x * (-1)**(math.ceil(pos_x)) # expands range to random number between -10 and 10
        pos_y = random.random() * 10 # uniformly distributed random number between 0 and 10
        pos_y = pos_y * (-1)**(math.ceil(pos_y)) # expands range to random number between -10 and 10
        
        return (pos_x, pos_y)
        
    # End def
    
    
    def get_direction(self):
        """Determines the direction the dot should move by comparing x and y values to thresholds"""
        # Default action: no movement
        x_dir = NONE
        y_dir = NONE
        
        # get x and y values from MPU
        (pos_x, pos_y) = self.get_imu_value()
        
        # update directions based on thresholds
        if (pos_x) < -self.thres_x:
            x_dir = LEFT
        if (pos_x) > self.thres_x:
            x_dir = RIGHT
            
        if (pos_y) < -self.thres_y:
            y_dir = DOWN
        if (pos_y) > self.thres_y:
            y_dir = UP
            
        return (x_dir, y_dir)
        
    # End def
    
# End class
        
        