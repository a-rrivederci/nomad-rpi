import pyrebase
import threading
import time
import sys

from api import Rover

DB = None
ROVER = None

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

    # Set next timer for 1Hz
    set_timer(1)
    return

def set_timer(timeout):
    timer = threading.Timer(timeout, update_sensor_data)
    timer.start()

def stream_handler(message):
    global ROVER
    print(message["data"])
    for x in message["data"]:
        if message["data"][x]:
            if x == "up":
                # move rover up
                ROVER.forward()
            elif x == "down":
                # move rover down
                ROVER.back()
            elif x == "right":
                # move rover right
                ROVER.right()
            elif x == "left":
                # move rover left
                ROVER.left()


def main():
    global DB
    global ROVER
    firebase = pyrebase.initialize_app(config)

    # Database variable
    DB = firebase.database()

    # Initialize rover
    ROVER = Rover()
    if not ROVER.connect():
        print("Failed to connect to NOMAD Rover.")
        sys.exit(1)

    # Read firebase stream
    DB.child("rpi").child("movement").stream(stream_handler)

    # Update firebase data and set the frequency to 1Hz
    set_timer(1)

    # If Loop
    while True:
        pass

    return


if __name__ == "__main__":
    main()
