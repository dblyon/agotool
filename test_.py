import unittest

class TestStringMethods(unittest.TestCase):

  def test_upper(self):
      self.assertEqual('foo'.upper(), 'FOO')

  def test_2(self):
      self.assertIs([], type(list))

if __name__ == '__main__':
    unittest.main()