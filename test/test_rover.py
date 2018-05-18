import unittest
from api.rover import Rover

class TestRover(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.rov = Rover()
    
    def test_import(self):
        '''Check the baudrate and end character from the current protocol'''
        self.assertEqual(self.rov.BAUDRATE, 9600)
        self.assertEqual(self.rov.READY_CHAR, "~")
        
    def test_sensor_data(self):
        ''' Check data being received from sensor command. '''
        pass

if __name__ == "__main__":
    unittest.main()
