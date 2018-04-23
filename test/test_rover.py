import unittest
from api.rover import Rover

class TestRover(unittest.TestCase):

    def setUp(self):
        self.rov = Rover()
    
    def test_import(self):
        """Check the baudrate and end character from the current protocol"""
        self.assertEqual(self.rov.BAUDRATE, 9600)
        self.assertEqual(self.rov.END_CHAR, "~")
        

if __name__ == "__main__":
    unittest.main()
