import unittest
from pyloc import LOCCountDir

class TestAssignamentDos(unittest.TestCase):
    def test_CountUno(self):
        print "In method", self._testMethodName
        LOCCountDir('../assignament1/')
    def test_CountDos(self):
        print "In method", self._testMethodName
        LOCCountDir('../assignament2/')

if __name__ == '__main__':
    unittest.main()