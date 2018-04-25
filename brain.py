import pyrebase
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
    left_ir, mid_ir, right_ir = ROVER.sensor()
    # Package message
    data = {
        "leftIR":left_ir,
        "midIR":mid_ir,
        "rightIR":right_ir,
    }
    # Update fields in firebase
    DB.child("rpi").child("data").update(data)
    return

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

    # Database Variable
    DB = firebase.database()

    # initialize rover
    ROVER = Rover()
    if not ROVER.connect():
        print("Failed to connect to NOMAD Rover.")
        exit(1)

    DB.child("rpi").child("movement").stream(stream_handler)
    return


if __name__ == "__main__":
    main()
