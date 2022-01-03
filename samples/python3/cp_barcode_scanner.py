#!/usr/bin/env python3
""" Sample application for pixycamev3

Use this example on LEGO EV3 brick running ev3dev.

This Python3 example scans Pixy barcodes one at a time
and names them.

Download the barcodes from the Pixy2 wiki:
https://pixycam.com/downloads-pixy2/

Building instructions:
- LEGO EV3 brick running ev3dev
- Connect Pixy2 to port 1
- Set I2C address to 0x54
- Connect LEGO TouchSensor to port 4

Author  : Kees Smit
Date    : December 29 2021
Version : 1.00
License : GNU General Public License v2

Charmed Labs, www.charmedlabs.com
"""
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound
from pixycamev3.pixy2 import Pixy2, MainFeatures

def main():

    touch_4 = TouchSensor(INPUT_4)
    sound = Sound()
    pixy2 = Pixy2(port=1, i2c_address=0x54)
    data = MainFeatures()
    
    # Toggle lamp pixy on
    pixy2.set_lamp(1, 0)
    
    # Loop until TouchSensor is pressed
    while not touch_4.value():
        # Get linetracking data from pixy2
        data = pixy2.get_linetracking_data()
        # Process data
        if data.error:
            # Data error: unkown feature type, try reading again
            pass
        else:
            if data.number_of_barcodes > 0:
                # Barcode detected, say which number it has
                sound.speak(data.barcodes[0].code)
        # Clear data for reading next loop
        data.clear()
    
    # Toggle lamp off
    pixy2.set_lamp(0, 0)

if __name__ == '__main__':
    main()