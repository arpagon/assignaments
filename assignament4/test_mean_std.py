import unittest
from mean_std import Mean, Std, LinkedList

class TestAssignament(unittest.TestCase):
    def test_estimate_proxy_size(self):
        a=LinkedList([160,591,114,229,230,270,128,1657,624,1503])
        print "---------------------------------------"
        print "In method", self._testMethodName
        print a
        print("%.2f" % Mean(a))
        print("%.2f" % Std(a))
    
    def test_development_hours(self):
        print "---------------------------------------"
        print "In method", self._testMethodName
        a=LinkedList([15.0,69.9,6.5,22.4,28.4,65.9,19.4,198.7,38.8,138.2])
        print a
        print("%.2f" % Mean(a))
        print("%.2f" % Std(a))

if __name__ == '__main__':
    unittest.main()