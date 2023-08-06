import unittest

from utilset import string


class TestString(unittest.TestCase):

    def test_concat(self):
        self.assertEqual(string.concat("a", "b", "c"), "abc")


if __name__ == '__main__':
    unittest.main()