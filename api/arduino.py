#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""\
Classes to easily communicate with Arduino.

since: 23-APR-2018
"""

import io
import re
import serial
import serial.tools.list_ports

class Arduino(object):
    """Class to connect and interface with an Arduino Uno."""
    def __init__(self, baudrate):
        self.status = None
        self.conn = None
        self.port = None
        self.baudrate = baudrate
    
    def connect(self):
        """Connect to 'closest' arduino device"""
        # Get likely arduino connection
        seq = re.compile(r'/dev/ttyACM[0-9]|COM[0-9]')
        ports = list(serial.tools.list_ports.comports())

        if ports == []:
            self.status = "No ports found"
            # exit if no connection
            return False
    
        for portString in ports:
            # If ACM or Arduino is found in string
            if ('ACM' in str(portString)) or ('Arduino' in str(portString)):
                # Find out com port and connect
                self.port = seq.match(str(portString)).group()
                self.conn = serial.Serial(self.port, self.baudrate)
                self.status = "Connected to Arduino"
                return True

        self.status = "No Arduino found"
        return False

    def send_str_data(self, string):
        """Send character string"""
        self.conn.write(string.encode('utf-8'))
        return

    def read_str_data(self):
        """Read string"""
        data = self.conn.readline()
        return data.decode().rstrip()

    def read_num_data(self):
        """Reads in numerical data from uno"""
        data = self.conn.readline()
        return ord(data.decode().rstrip())

    def clear_buffer(self):
        """Flush serial buffer"""
        self.conn.flushInput()
        self.conn.flushOutput()
        return

    def __del__(self):
        if self.conn:
            self.conn.close()
        return
