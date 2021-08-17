import unittest

from different import function_to_be_tested


class MyFirstTest(unittest.TestCase):

    def test(self):
        self.assertIsInstance(function_to_be_tested(7), str, 'Output of Function Should br STR.')


if __name__ == '__main__':
    unittest.main()