import pyrebase
import sys

from api import Rover

# DB = None
# ROVER = None

# config = {
#     "apiKey": "AIzaSyDKstoSby1YdpTfy7xqAiDPt5Ta50PoOIw",
#     "authDomain": "nomad-e1934.firebaseapp.com",
#     "databaseURL": "https://nomad-e1934.firebaseio.com",
#     "projectId": "nomad-e1934",
#     "storageBucket": "nomad-e1934.appspot.com",
# }

# # def getState():
# #     global DB
# #     currentState = DB.child("PiMove").get()

# def stream_handler(message):
#     global DB
#     global ROVER
#     sens1, sens2, sens3 = ROVER.sensor()
#     batt_lvl = ROVER.battery()
#     data = {"Sensor1":sens1, "Sensor2":sens2, "Sensor3":sens3, "Battery":batt_lvl}
#     DB.child("PiMove").child("Sensors").set(data)
#     print(message["data"])
#     for x in message["data"]:
#         if message["data"][x]:
#             if x == "up":
#                 # move rover up
#                 ROVER.forward()
#             elif x == "down":
#                 # move rover down
#                 ROVER.back()
#             elif x == "right":
#                 # move rover right
#                 ROVER.right()
#             elif x == "left":
#                 # move rover left
#                 ROVER.left()


# def main():
#     global DB
#     global ROVER
#     firebase = pyrebase.initialize_app(config)

#     # Database Variable
#     DB = firebase.database()

#     # currentState = ""

#     # initialize rover
#     ROVER = Rover()
#     if not ROVER.connected:
#         print("Failed to connect to NOMAD Rover.")
#         exit(1)

#     DB.child("PiMove").child("Movement").stream(stream_handler)

# if __name__ == "__main__":
#     main()
