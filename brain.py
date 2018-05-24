import os
import sys
import logging
import functools
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

def catch_abort(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Caught an {e} in {f.__name__}")
            sys.exit(1)
    return func

class Brain(object):
    '''Raspberry Pi control center'''

    def __init__(self):
        self.LOG = logging.getLogger(f"{__name__}.{__class__.__name__}")

        # Class variables
        self.interval = 5 # secs
        self.continue_timer = None

        # Class objects
        self.data_timer = Timer(self.interval, self.update_sensor_data)
        self.rover = Rover()
        self.db = Firebase().database

        if not self.rover.connect():
            self.LOG.info("Failed to connect to NOMAD Rover.")
            sys.exit(1)

    @catch_abort
    def control_handler(self, msg: dict) -> None:
        '''Control the follow and update of data'''

        self.LOG.debug(msg)

        if msg["path"] == "/":
            self.LOG.info(msg["data"])
            # Initial pass to ensure data is not sent
            self.continue_timer = False

            if msg["data"]["active"] == True:
                # Start data sender
                self.data_timer.start()
                self.continue_timer = True

            elif msg["data"]["active"] == False:
                # Start data sender
                self.continue_timer = False

            else: # unrecognized message
                self.LOG.info(msg)

        else: # unrecognized message
            self.LOG.info(msg)

        self.LOG.info(f"Timer continue status: {self.continue_timer}")
        
        return

    @catch_abort
    def movement_handler(self, msg: dict) -> None:
        '''Track and handle changes in the 'movement' node of the database'''

        self.LOG.debug(msg)

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
    
    @catch_abort
    def update_sensor_data(self) -> None:
        '''Update all the sensor data in firebase'''
        # Get sensor data
        data = self.rover.get_sensors()

        # Update fields in firebase
        self.db.child("data").update(data)

        # Restart timer
        self.LOG.debug(f"Data timer status: {self.data_timer.finished}")
        if self.data_timer.finished and self.continue_timer == True:
            self.data_timer = Timer(self.interval, self.update_sensor_data)
            self.data_timer.start()

        return
    
    @catch_abort
    def start_thinking(self) -> None:
        '''Enter the matrix'''

        # Set data control handler
        self.db.child("control").stream(self.control_handler)
        # Set movement handler
        self.db.child("movement").stream(self.movement_handler)

        # Start message
        self.LOG.info("Entering the Matrix ...\n")


if __name__ == "__main__":
    BRAIN = Brain()
    BRAIN.start_thinking()
