import unittest

from zvolv_sdk import divide_by_three


class TestDivideByThree(unittest.TestCase):

	def test_divide_by_three(self):
		self.assertEqual(divide_by_three(12), 4)

unittest.main()