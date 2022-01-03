#!/usr/bin/env pybricks-micropython
""" Sample application for pixycamev3

Use this example on LEGO EV3 brick running pybricks-micropython.

This example is a linetracking application.
You can improve this example by adding a PID-controller,
for simplicity a PID is left out now.

Standard behavior at an intersection is to go straight, but
you can change this behaviour with the aid of two Pixy barcodes:
- barcode 0: turn left at the first intersection
- barcode 5: turn right at the first intersection
Download the barcodes from the Pixy2 wiki:
https://pixycam.com/downloads-pixy2/

If your robot drives in the wrong direction you need to change
the polarity of the motors: set argument positive_direction
to Direction.CLOCKWISE.

If your robot seems to turn to the wrong direction (move
from the line instead of following it), you probable need to
switch ports for the motors.

Building instructions:
- LEGO EV3 brick running pybricks-micropython
- Connect Pixy2 to port 1
- Set I2C address to 0x54
- Connect LEGO TouchSensor to port 4
- Connect two LEGO LargeMotors to ports A and D

Author  : Kees Smit
Date    : December 29 2021
Version : 1.00
License : GNU General Public License v2

Charmed Labs, www.charmedlabs.com
"""
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port, Direction
from pixycamev3.pixy2 import Pixy2, MainFeatures

class Robot:
    def __init__(self):
        # Connect TouchSensor
        self.brick = EV3Brick()
        self.touch_4 = TouchSensor(Port.S4)
        # Connect motors
        self.motor_a = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
        self.motor_d = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)
        # State of robot
        self._basic_speed = 500
        self._GAIN = 30

    def move(self, speed_x):
        """Move robot when in _ACTIVE mode."""
        speed_x *= self._GAIN
        speed_a = limit_speed(self._basic_speed - speed_x)
        speed_d = limit_speed(self._basic_speed + speed_x)
        self.motor_a.run(speed_a)
        self.motor_d.run(speed_d)
    
    def stop(self):
        """Stop robot."""
        self.motor_a.stop()
        self.motor_d.stop()


def limit_speed(speed):
  """Limit speed in range [-900,900]."""
  if speed > 1000:
    speed = 1000
  elif speed < -1000:
    speed = -1000
  return speed

def main():

    # Defining reference point
    X_REF = 39   # X-center coordinate of view

    ev3 = Robot()
    pixy2 = Pixy2(port=1, i2c_address=0x54)
    data = MainFeatures()
    
    # Toggle lamp pixy on
    pixy2.set_lamp(1, 0)
    
    # Loop until TouchSensor is pressed
    while not ev3.touch_4.pressed():
        # Get linetracking data from pixy2
        data = pixy2.get_linetracking_data()
        # Process data
        if data.error:
            # Data error: unkown feature type, try reading again
            pass
        else:
            if data.number_of_barcodes > 0:
                # Barcode(s) found
                for i in range(0, data.number_of_barcodes):
                    if data.barcodes[i].code == 5:
                        # Turn right at first intersection
                        ev3.brick.speaker.say('Right')
                        pixy2.set_next_turn(-90)
                    elif data.barcodes[i].code == 0:
                        # Turn left at first intersection
                        ev3.brick.speaker.say('Left')
                        pixy2.set_next_turn(90)
        if data.number_of_vectors > 0:
            dx = X_REF - data.vectors[0].x1
            ev3.move(dx)
        else:
            # No vector data, stop robot
            ev3.stop()
        # Clear data for reading next loop
        data.clear()
    
    # Toggle lamp off
    pixy2.set_lamp(0, 0)

    # Turn motors off
    ev3.stop()

if __name__ == '__main__':
    main()