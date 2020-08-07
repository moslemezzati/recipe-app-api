from django.test import TestCase

from app.calc import add, subtract

class CalcTest(TestCase):

  def test_add_numbers(self):
    """Test that two numbers are added together"""
    self.assertEqual(add(1,5), 6)
  
  def test_subtract_numbers(self):
    """Test that two numbers are subtracted"""
    self.assertEqual(subtract(4, 3), 1)