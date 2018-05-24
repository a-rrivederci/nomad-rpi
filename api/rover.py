#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''\
Implementation specific program for the nomad rover

since: 23-APR-2018
'''

import re
import sys
import datetime
from time import sleep
import logging
from .arduino import ArduinoUno

ROOT_LOGGER = logging.getLogger(__name__)
ROOT_LOGGER.setLevel(level=logging.DEBUG)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMATTER = logging.Formatter(
    fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
    datefmt='%H:%M:%S'
)
LOG_HANDLER.setFormatter(LOG_FORMATTER)
ROOT_LOGGER.addHandler(LOG_HANDLER)


class Rover(object):
    '''Nomad Rover application center'''

    def __init__(self, baudrate: int = 9600):
        self.ROV_LOG = logging.getLogger(f"{__name__}.py")
        self.MCU_LOG = logging.getLogger(f"{__name__}.uno")
    
        self.ARDUINO = None
        self.BAUDRATE = baudrate
        self.ptime = 0.1

        # Comms protocols
        self.ASSERT_CHAR = '>'
        self.NOT_ASSERT_CHAR = '<'
        self.READY_CHAR = '~'

        # Commands
        self.STOP = "A\n"
        self.FWRD = "B\n"
        self.BACK = "C\n"
        self.RGHT = "D\n"
        self.LEFT = "E\n"
        self.SENS = "F\n"

        self.ROV_LOG.info(f"Initialized {__class__.__name__}")

    def connect(self) -> bool:
        '''Establish connection with the mcu'''
        ret = False
        self.ARDUINO = ArduinoUno()
        if self.ARDUINO.connect():
            self.get_response()
            ret = True
        return ret

    def move(self, direction: str, time: int=0.1) -> None:
        # Send command
        self.ARDUINO.flush_buffers()
        self.pause()
        self.ARDUINO.send_str(direction)
        self.pause()

        # Get response
        self.get_response()

        return
        
    def pause(self, time: int=0.1) -> None:
        sleep(time)

        return

    def get_sensors(self) -> dict:
        '''Sensors method'''
        cmd = self.SENS

        # Send command
        self.ARDUINO.flush_buffers()
        self.pause()
        self.ARDUINO.send_str(cmd)
        self.pause()

        # "Get response"
        # Get and process sensor data
        data = {}
        while True:
            line = self.ARDUINO.read_str(strip=1)
            if line == self.ASSERT_CHAR:
                self.ROV_LOG.info(f"Asserted {line}\n")
            elif line == self.READY_CHAR:
                break
            else:
                label, value = line.split(':')
                data[label] = int(value)

        self.ROV_LOG.info(f"Data: {data}")

        return data

    def get_response(self):
        '''Continously log all data on the port until protocol end'''
        while True:
            line = self.ARDUINO.read_str()
            if line == self.ASSERT_CHAR:
                self.ROV_LOG.info(f"Asserted {line}\n")
            elif line == self.READY_CHAR:
                break
            else:
                self.MCU_LOG.info(line)

if __name__ == "__main__":
    rover = Rover()
    sys.exit(0)
