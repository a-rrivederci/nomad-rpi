import unittest
from api.rover import Rover

NUM_SENSORS = 3

class TestRover(unittest.TestCase):

    def setUp(self):
        self.rov = Rover()
    
    def test_import(self):
        """Check the baudrate and end character from the current protocol"""
        self.assertEqual(self.rov.BAUDRATE, 9600)
        self.assertEqual(self.rov.END_CHAR, "~")
        
    def test_sensor_data(self):
        """ Check data being received from sensor command. """
        cmd = self.rov.SENS
        self.rov.ARDUINO.clear_buffer()

        # Send command
        self.rov.ARDUINO.send_str_data(cmd)
        
        # Get sensor data
        msg = ""
        while True:
            m = self.rov.ARDUINO.read_str_data()
            if m == self.rov.END_CHAR:
                break
            else:
                msg += m

        self.assertEqual(msg.find('Asserted'), 0)
        self.assertEqual(len(msg.count(':')), NUM_SENSORS)

if __name__ == "__main__":
    unittest.main()
