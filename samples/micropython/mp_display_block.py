#!/usr/bin/env pybricks-micropython
""" Sample application for pixycamev3

Use this example on LEGO EV3 brick running pybricks-micropython.

This example application detects blocks for sig=1 and
displays these blocks as a rectangle on the EV3 display.

Building instructions:
- LEGO EV3 brick running pybricks-micropython
- Connect Pixy2 to port 1
- Set I2C address to 0x54
- Connect LEGO TouchSensor to port 4

Author  : Kees Smit
Date    : December 29 2021
Version : 1.00
License : GNU General Public License v2

Charmed Labs, www.charmedlabs.com
"""
from time import sleep

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import TouchSensor
from pybricks.parameters import Port
from pixycamev3.pixy2 import Pixy2

ev3 = EV3Brick()
ts = TouchSensor(Port.S4)

# Pixy2 connected to port 1, i2c address set to 0x54
pixy2 = Pixy2(port=1, i2c_address=0x54)

# Display detected blocks on EV3 display
while not ts.pressed():
    # Clear display
    ev3.screen.clear()
    # Request blockdata for sig=1, max 1 block
    nr_blocks, block = pixy2.get_blocks(1, 1)
    # Extract data
    if nr_blocks > 0:
        sig = block[0].sig
        x = block[0].x_center
        y = block[0].y_center
        w = block[0].width
        h = block[0].height
        # Scale to resolution of EV3 display
        x *= 0.6
        y *= 0.6
        w *= 0.6
        h *= 0.6
        # Calculate rectangle to draw in display
        dx = int(w/2)
        dy = int(h/2)
        xa = x - dx
        ya = y + dy
        xb = x + dx
        yb = y- dy
        # Draw rectangle
        ev3.screen.draw_box(xa, ya, xb, yb, fill=True)
        sleep(0.1)