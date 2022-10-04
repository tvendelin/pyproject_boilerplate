import unittest
import mymodule


class TestMyModule(unittest.TestCase):
    def test_dummy(self):
        actual = mymodule.return_a_string()
        self.assertEqual(actual, "Ohoo!")
