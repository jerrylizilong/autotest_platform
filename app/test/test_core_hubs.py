from app.core import hubs
import unittest

class TestHubs(unittest.TestCase):
    def test_show_hubs(self):
        hubCount =len(hubs.hubs().showHubs(''))
        self.assertEqual((hubCount>0),True)


if __name__ == '__main__':
    unittest.main()