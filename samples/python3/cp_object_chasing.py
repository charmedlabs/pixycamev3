#!/usr/bin/env python3
""" Sample application for pixycamev3

Use this example on LEGO EV3 brick running ev3dev.

This Python3 example shows how to chase a detected object.

On the wiki you'll find an explanation how chasing an object works.
Have a look at:
https://docs.pixycam.com/wiki/doku.php?id=wiki:v2:lego_chase_demo

If your robot drives in the wrong direction you need to change
the polarity of the motors. If your robot seems to turn to the
wrong direction (turn away from the object instead of facing it),
you probable need to switch ports for the motors.

This example uses an PID-controller. You may have to adjust the
values for the PID-constants for your robot.

Building instructions:
- LEGO EV3 brick running ev3dev
- Connect Pixy2 to port 1
- Set I2C address to 0x54
- Set signature 1 for the object you like to follow
- Connect LEGO TouchSensor to port 4
- Connect two LEGO LargeMotors to ports A and D

Author  : Kees Smit
Date    : December 29 2021
Version : 1.00
License : GNU General Public License v2

Charmed Labs, www.charmedlabs.com
"""
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D
from pixycamev3.pixy2 import Pixy2 

def limit_speed(speed):
    """ Limit speed in range [-1000,1000] """
    if speed > 1000:
        speed = 1000
    elif speed < -1000:
        speed = -1000
    return speed

def main():
    # Connect Pixy2
    pixy2 = Pixy2(port=1, i2c_address=0x54)
    
    # Signatures we're interested in (SIG1)
    sig = 1
    
    # Connect TouchSensor (to stop script)
    ts = TouchSensor(INPUT_4)
    
    # Connect LargeMotors
    rmotor = LargeMotor(OUTPUT_A)
    lmotor = LargeMotor(OUTPUT_D)
    
    # Adjust polarity motors (depending on the build of your robot)
    rmotor.polarity = LargeMotor.POLARITY_INVERSED
    lmotor.polarity =LargeMotor.POLARITY_INVERSED

    # Defining constants
    X_REF = 158  # X-coordinate of referencepoint
    Y_REF = 150  # Y-coordinate of referencepoint
    KP = 0.4     # Proportional constant PID-controller
    KI = 0.01    # Integral constant PID-controller
    KD = 0.05    # Derivative constant PID-controller
    GAIN = 10    # Gain for motorspeed
    
    # Initializing PID variables
    integral_x = 0
    derivative_x = 0
    last_dx = 0
    integral_y = 0
    derivative_y = 0
    last_dy = 0
    
    while not ts.value():
        # Request block
        nr_blocks, block = pixy2.get_blocks(1, 1)
        # Extract data
        if nr_blocks > 0:
            # SIG1 detected, control motors
            x = block[0].x_center         # X-centrois of object
            y = block[0].y_center         # Y-centroid of object
            dx = X_REF - x                # Error in reference to X_REF
            integral_x = integral_x + dx  # Calculate integral for PID
            derivative_x = dx - last_dx   # Calculate derivative for PID
            speed_x = KP*dx + KI*integral_x + KD*derivative_x  # Speed X-direction
            dy = Y_REF - y                # Error in reference to Y_REF
            integral_y = integral_y + dy  # Calculate integral for PID
            derivative_y = dy - last_dy   # Calculate derivative for PID
            speed_y = KP*dy + KI*integral_y + KD*derivative_y  # Speed Y-direction
            # Calculate motorspeed out of speed_x and speed_y
            # Use GAIN otherwise speed will be to slow,
            # but limit in range [-1000,1000]
            rspeed = limit_speed(GAIN*(speed_y - speed_x))
            lspeed = limit_speed(GAIN*(speed_y + speed_x))
            rmotor.run_forever(speed_sp = round(rspeed))
            lmotor.run_forever(speed_sp = round(lspeed))
            last_dx = dx                  # Set last error for x
            last_dy = dy                  # Set last error for y
        else:
            # SIG1 not detected, stop motors
            rmotor.stop()
            lmotor.stop()
            last_dx = 0
            last_dy = 0
    
    # TouchSensor pressed, stop motors
    rmotor.stop()
    lmotor.stop()

if __name__ == '__main__':
    main()