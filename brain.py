import pyrebase
import sys
import logging

from api import Rover

DB = None
ROVER = None

ROOT_LOGGER = logging.getLogger("nomad")
ROOT_LOGGER.setLevel(level=logging.INFO)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMATTER = logging.Formatter(
    fmt='%(asctime)s [%(name)s](%(levelname)s) %(message)s',
    datefmt='%H:%M:%S'
)
LOG_HANDLER.setFormatter(LOG_FORMATTER)
ROOT_LOGGER.addHandler(LOG_HANDLER)

LOGGER = logging.getLogger("nomad.brain")

# firebase configuration
config = {
    "apiKey": "AIzaSyD9QEbkOyk0B25L3s7X1T_wfBNuLrOyCuc",
    "authDomain": "nomad-fire.firebaseapp.com",
    "databaseURL": "https://nomad-fire.firebaseio.com",
    "projectId": "nomad-fire",
    "storageBucket": "nomad-fire.appspot.com",
    "messagingSenderId": "1097082057466"
}

def update_sensor_data():
    """Update all the sensor data in firebase"""
    global DB
    global ROVER

    # Get sensor data
    data = ROVER.sensor()
    
    # Update fields in firebase
    DB.child("rpi").child("data").update(data)
    return

def stream_handler(message):
    global ROVER
    if message["path"] == "/":
        LOGGER.info(message["data"])
    elif message["data"] == True:
        if message["path"] == "/forward":
            ROVER.forward()
        elif message["path"] == "/backward":
            ROVER.back()
        elif message["path"] == "/right":
            ROVER.right()
        elif message["path"] == "/left":
            ROVER.left()
        else: # unrecognized message
            LOGGER.info(message)
    else: # unrecognized message
        LOGGER.info(message)

def main():
    global DB
    global ROVER
    firebase = pyrebase.initialize_app(config)

    # Database Variable
    DB = firebase.database()

    # initialize rover
    ROVER = Rover()
    if not ROVER.connect():
        LOGGER.info("Failed to connect to NOMAD Rover.")
        exit(1)

    DB.child("rpi").child("movement").stream(stream_handler)
    return

if __name__ == "__main__":
    main()
