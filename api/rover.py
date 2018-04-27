#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""\
Rover class to send commands and read data from to the microcontroller.

since: 23-APR-2018
"""

import re
import sys
import datetime
from time import sleep
import logging
from .arduino import Arduino

ROOT_LOGGER = logging.getLogger("nomad")
ROOT_LOGGER.setLevel(level=logging.INFO)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMATTER = logging.Formatter(
    fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
    datefmt='%H:%M:%S'
)
LOG_HANDLER.setFormatter(LOG_FORMATTER)
ROOT_LOGGER.addHandler(LOG_HANDLER)

PY_LOGGER = logging.getLogger("nomad.rover")
MCU_LOGGER = logging.getLogger("nomad.arduino")

class Rover(object):
    """\
    Nomad Rover instructional. 
    """
    def __init__(self):
        self.ARDUINO = None
        self.BAUDRATE = 9600
        self.END_CHAR = "~"

        # Commands
        self.STOP = "A\n"
        self.FWRD = "B\n"
        self.BACK = "C\n"
        self.RGHT = "D\n"
        self.LEFT = "E\n"
        self.SENS = "F\n"
    
    def connect(self):
        # Establish connection with the Firmware
        self.ARDUINO = Arduino(self.BAUDRATE)
        if self.ARDUINO.connect():
            self.print_data()
            return True
        return False

    def forward(self):
        """Foward method."""
        cmd = self.FWRD
        self.ARDUINO.clear_buffer()

        # Send command
        self.ARDUINO.send_str_data(cmd)
        sleep(0.1)

    def back(self):
        """Bacward method."""
        cmd = self.BACK
        self.ARDUINO.clear_buffer()

        # Send command
        self.ARDUINO.send_str_data(cmd)
        sleep(0.1)

    def right(self):
        """Right method."""
        cmd = self.RGHT
        self.ARDUINO.clear_buffer()

        # Send command
        self.ARDUINO.send_str_data(cmd)
        sleep(0.1)

    def left(self):
        """Left method."""
        cmd = self.LEFT
        self.ARDUINO.clear_buffer()

        # Send command
        self.ARDUINO.send_str_data(cmd)
        sleep(0.1)

    def sensor(self):
        """Sensors method."""
        cmd = self.SENS
        self.ARDUINO.clear_buffer()

        # Send command
        self.ARDUINO.send_str_data(cmd)
        
        # Get sensor data
        msg = ""
        while True:
            m = self.ARDUINO.read_str_data()
            if m == self.END_CHAR:
                break
            else:
                msg += m + "\n"

        # sensor data
        data = {}
        for sens in msg.split('\n')[1:-1]:
            name, val = [i.strip() for i in sens.split(':')]
            data[name] = int(val)
        PY_LOGGER.info("Data: {}".format(data))
        return data

    def print_data(self):
        """Print received data."""
        while True:
            msg = self.ARDUINO.read_str_data()
            if msg == self.END_CHAR:
                break
            else:
                MCU_LOGGER.info(msg)

if __name__ == "__main__":
    rover = Rover()
    sys.exit(0)
