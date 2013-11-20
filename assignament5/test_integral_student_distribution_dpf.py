import unittest
from integral_student_distribution_dpf import IntegrateSimpsonRule

class TestAssignament(unittest.TestCase):
	#test_one:
	def test_one(self):
		#IntegrateSimpsonRule(1.1, 9)
		result, E, steps = IntegrateSimpsonRule(1.1, 9)
		#print result
		#espected_result = 0.35006
		print ("result: %s \n"
				"espected_result = 0.35006" % result)

	#test_two:
	def test_two(self):
		#IntegrateSimpsonRule(1.1812, 10)
		result, E, steps = IntegrateSimpsonRule(1.1812, 10)
		#print result
		#espected_result = 0.36757
		print ("result: %s \n"
				"espected_result = 0.36757" % result)
	def test_three(self):
		#IntegrateSimpsonRule(2.750, 30)
		result, E, steps = IntegrateSimpsonRule(2.750, 30)
		#print result
		#espected_result = 0.49500
		print ("result: %s \n"
				"espected_result = 0.49500" % result)


if __name__ == '__main__':
    unittest.main()