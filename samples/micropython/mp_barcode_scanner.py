#!/usr/bin/env pybricks-micropython
""" Sample application for pixycamev3

Use this example on LEGO EV3 brick running pybricks-micropython.

This example scans Pixy barcodes one at a time and names them.

Download the barcodes from the Pixy2 wiki:
https://pixycam.com/downloads-pixy2/

Building instructions:
- LEGO EV3 brick running pybricks-micropython.
- Connect Pixy2 to port 1
- Set I2C address to 0x54
- Connect LEGO TouchSensor to port 4

Author  : Kees Smit
Date    : December 29 2021
Version : 1.00
License : GNU General Public License v2

Charmed Labs, www.charmedlabs.com
"""
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import TouchSensor
from pybricks.parameters import Port
from pixycamev3.pixy2 import Pixy2, MainFeatures

def main():

    ev3 = EV3Brick()
    touch_4 = TouchSensor(Port.S4)
    pixy2 = Pixy2(port=1, i2c_address=0x54)
    data = MainFeatures()
    
    # Toggle lamp pixy on
    pixy2.set_lamp(1, 0)
    
    # Loop until TouchSensor is pressed
    while not touch_4.pressed():
        # Get linetracking data from pixy2
        data = pixy2.get_linetracking_data()
        # Process data
        if data.error:
            # Data error: unkown feature type, try reading again
            pass
        else:
            if data.number_of_barcodes > 0:
                # Barcode detected, say which number it has
                ev3.speaker.say(str(data.barcodes[0].code))
        # Clear data for reading next loop
        data.clear()
    
    # Toggle lamp off
    pixy2.set_lamp(0, 0)

if __name__ == '__main__':
    main()