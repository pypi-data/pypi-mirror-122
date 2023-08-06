# -----------------------------------------------------------------------------
# - File              usbswsdk_unittest.py
# - Owner             Zhengkun Li
# - Version           1.0
# - Date              09.06.2021
# - Classification    usbswsdk_unittest
# - Brief             usbswsdk_unittest for ZD USB Switch
# ----------------------------------------------------------------------------- 
import unittest
from zuss import *
comport = "COM3"
class TestTemplate(unittest.TestCase):
    def test_set_host_port(self):
        a = set_host_port(comport,3)
        self.assertTrue(a)
        a = set_host_port(comport,5)
        self.assertFalse( a)
    def test_get_host_port(self):
        set_host_port(comport,3)
        a = get_host_port(comport)
        self.assertEqual("3",a)
        set_host_port(comport,1)
        a = get_host_port(comport)
        self.assertEqual("1",a)
    def test_set_dev_port(self):
        a = set_dev_port(comport,1)
        self.assertTrue(a)
        a = set_dev_port(comport,2)
        self.assertTrue(a)
        a = set_dev_port(comport,3)
        self.assertTrue(a)
        a = set_dev_port(comport,4)
        self.assertTrue(a)
        a = set_dev_port(comport,5)
        self.assertFalse( a)
    def  test_get_dev_port(self):
        set_dev_port(comport,3)
        a = get_dev_port(comport)
        self.assertEqual("3",a)
        set_dev_port(comport,1)
        a = get_dev_port(comport)
        self.assertEqual("1",a)
    def test_set_relay_mask(self):
        for i in range(0,15):   
            a = set_relay_mask(comport,i)
            self.assertTrue( a)
    def test_get_relay_mask(self):
        for i in range(0,15):   
            set_relay_mask(comport,i)
            a = get_relay_mask(comport)
            self.assertEqual(i, a)
    def test_set_pwr_mask(self):
        for i in range(0,15):   
            a = set_pwr_mask(comport,i)
            self.assertTrue( a)
    def test_get_pwr_mask(self):
        for i in range(0,15):   
            set_pwr_mask(comport,i)
            a = get_pwr_mask(comport)
            self.assertEqual(i, a)
if __name__ == '__main__':
    unittest.main()