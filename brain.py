import os
import sys
import logging
from threading import Timer

from api import Rover
from api import Firebase


ROOT = logging.getLogger(__name__)
ROOT.setLevel(level=logging.DEBUG)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMATTER = logging.Formatter(
    fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
    datefmt='%H:%M:%S'
)
LOG_HANDLER.setFormatter(LOG_FORMATTER)
ROOT.addHandler(LOG_HANDLER)

class Brain(object):
    '''Raspberry Pi control center'''

    def __init__(self):
        self.LOG = logging.getLogger(f"{__name__}.{__class__.__name__}")

        # Class variables
        self.interval = 2 # secs

        # Class objects
        self.data_timer = Timer(self.interval, self.update_sensor_data)
        self.rover = Rover()
        self.db = Firebase().database

        if not self.rover.connect():
            self.LOG.info("Failed to connect to NOMAD Rover.")
            sys.exit(1)

    def movement_handler(self, msg: dict) -> None:
        '''Track and handle changes in the 'movement' node of the database'''
        self.LOG.info(msg)

        if msg["path"] == "/":
            self.LOG.info(msg["data"])
    
        elif msg["data"] == True:
            if msg["path"] == "/forward":
                self.rover.move(self.rover.FWRD)
    
            elif msg["path"] == "/backward":
                self.rover.move(self.rover.BACK)

            elif msg["path"] == "/right":
                self.rover.move(self.rover.RGHT)

            elif msg["path"] == "/left":
                self.rover.move(self.rover.LEFT)

            else: # unrecognized msg
                self.LOG.info(msg)

        else: # unrecognized msg
            self.LOG.info(msg)

        return
    
    def update_sensor_data(self) -> None:
        '''Update all the sensor data in firebase'''
        # Get sensor data
        data = self.rover.get_sensors()

        # Update fields in firebase
        self.db.child("data").update(data)

        # Restart timer
        self.data_timer.start()
        return
    
    def start_thinking(self) -> None:
        '''Enter the matrix'''
        # Set movement handler
        self.db.child("movement").stream(self.movement_handler)
        # Start data sender
        self.data_timer.start()
        self.LOG.info("Entering the Matrix ...\n")

        return


if __name__ == "__main__":
    BRAIN = Brain()
    BRAIN.start_thinking()
    sys.exit(0)
