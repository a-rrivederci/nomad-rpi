#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial.tools.list_ports
import re
import io
import os
import sys
import datetime
from time import sleep
import logging
import serial

class Arduino(object):
    def __init__(self, ability, port):
        self.name = ability
        self.conn = serial.Serial(port, 9600)

    def send_str_data(self, string):
        """ Send character string """
        self.conn.write(string.encode('utf-8'))

    def read_str_data(self):
        """ read string """
        data = self.conn.readline()
        return data.decode().rstrip()

    def read_num_data(self):
        """ Reads in numerical data from uno """
        data = self.conn.readline()
        return ord(data.decode().rstrip())

    def clear_buffer(self):
        """ Flush serial buffer """
        self.conn.flush()

    def __del__(self):
        self.conn.close()

class Rover(object):

    # command codes for Arduino
    CMD_STOP = "A" + "\n"
    CMD_FRWD = "B" + "\n"
    CMD_BACK = "C" + "\n"
    CMD_RGHT = "D" + "\n"
    CMD_LEFT = "E" + "\n"
    CMD_SENS = "F" + "\n"

    ROOT_LOGGER = logging.getLogger("nomad")
    ROOT_LOGGER.setLevel(level=logging.INFO)
    LOG_HANDLER = logging.StreamHandler()
    LOG_FORMATTER = logging.Formatter(
        fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
        datefmt='%H:%M:%S')
    LOG_HANDLER.setFormatter(LOG_FORMATTER)
    ROOT_LOGGER.addHandler(LOG_HANDLER)

    PY_LOGGER = logging.getLogger("nomad.rover")
    MCU_LOGGER = logging.getLogger("nomad.arduino")

    def __init__(self):
        self.debug = True
        self.arduino = None
        self.connected = False
        self.port = None
        # Get likely arduino connection
        seq = re.compile(r'/dev/ttyACM[0-9]|COM[0-9]')
        ports = list(serial.tools.list_ports.comports())
        if ports == []:
            Rover.PY_LOGGER.warning("No ports found")
        for portString in ports:
            # If uno is found in string
            if ('ACM' in str(portString) or 'Arduino' in str(portString)):
                # Find out com port and connect
                self.port = seq.match(str(portString)).group()
                self.arduino = Arduino("nomad", self.port)
                Rover.PY_LOGGER.info("Connected to Arduino")
                self.print_info()
                self.connected = True
        if not self.connected:
            Rover.PY_LOGGER.info("No Arduino found!")

    def forward(self):
        self.arduino.clear_buffer()

        if self.debug:
            Rover.PY_LOGGER.info("Sending {}".format(Rover.CMD_FRWD))
        
        # Send command
        self.arduino.send_str_data(Rover.CMD_FRWD)
        sleep(0.1)
        self.arduino.send_str_data(Rover.CMD_STOP)

    def back(self):
        self.arduino.clear_buffer()

        if self.debug:
            Rover.PY_LOGGER.info("Sending {}".format(Rover.CMD_BACK))
        
        # Send command
        self.arduino.send_str_data(Rover.CMD_BACK)
        sleep(0.1)
        self.arduino.send_str_data(Rover.CMD_STOP)

    def right(self):
        self.arduino.clear_buffer()

        if self.debug:
            Rover.PY_LOGGER.info("Sending {}".format(Rover.CMD_RGHT))
        
        # Send command
        self.arduino.send_str_data(Rover.CMD_RGHT)
        sleep(0.1)
        self.arduino.send_str_data(Rover.CMD_STOP)

    def left(self):
        self.arduino.clear_buffer()

        if self.debug:
            Rover.PY_LOGGER.info("Sending {}".format(Rover.CMD_LEFT))
        
        # Send command
        self.arduino.send_str_data(Rover.CMD_LEFT)
        sleep(0.1)
        self.arduino.send_str_data(Rover.CMD_STOP)

    def sensor(self):
        self.arduino.clear_buffer()

        if self.debug:
            Rover.PY_LOGGER.info("Sending {}".format(Rover.CMD_SENS))
        
        # Send command
        self.arduino.send_str_data(Rover.CMD_SENS)
        
        msg = ""
        while True:
            m = self.arduino.read_str_data()
            if m == '~':
                break
            else:
                msg += m

        # sensor data
        s1, s2, s3 = int(msg[2:5]), int(msg[5:8]), int(msg[8:11])
        Rover.PY_LOGGER.info("Sensor Data: {}, {}, {}".format(s1,s2,s3))
        return s1, s2, s3

    def battery(self):
        self.arduino.clear_buffer()

        if self.debug:
            Rover.PY_LOGGER.info("Sending {}".format(Rover.CMD_BATT))
        
        # Send command
        self.arduino.send_str_data(Rover.CMD_BATT)

        msg = ""
        while True:
            m = self.arduino.read_str_data()
            if m == '~':
                break
            else:
                msg += m

        battery_level = int(msg[2:])
        Rover.PY_LOGGER.info("Battery Level: {}".format(battery_level))
        return battery_level

    def print_info(self):
        while True:
            msg = self.arduino.read_str_data()
            if msg == '~':
                break
            else:
                Rover.MCU_LOGGER.info(msg)
