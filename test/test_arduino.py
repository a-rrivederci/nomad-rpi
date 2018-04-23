import unittest
import serial.tools.list_ports
from api.arduino import Arduino

class TestArduino(unittest.TestCase):
    def setUp(self):
        self.ard = Arduino(9600)

    def test_connection(self):
        """Test arduino module"""
        ports = list(serial.tools.list_ports.comports())

        if ports == []:
           self.assertFalse(self.ard.connect())
        else:
            for portString in ports:
                if ('ACM' in str(portString)) or ('Arduino' in str(portString)):
                    a = self.ard
                    a.connect()
                    # Read responses
                    self.assertEqual(a.read_str_data(), "NOMAD Uno v2.0.0")
                    self.assertEqual(a.read_str_data(), '~')
                else:
                    self.assertFalse(self.ard.connect())

if __name__ == '__main__':
    unittest.main()
