import unittest

from Morse.main import turnToMorse, turnToString, isValid


class MyTestCase(unittest.TestCase):
    def test_toMorse(self):
        result = turnToMorse('Hola Wilson')
        expected = '....;---;.-..;.-; ;.--;..;.-..;...;---;-.;'
        self.assertEqual(expected,result)  # add assertion here
    def test_ToString(self):
        result = turnToString('....;---;.-..;.-; ;.--;..;.-..;...;---;-.')
        expected = "HOLA WILSON"
        self.assertEqual(expected,result)
    def test_valid(self):
        result = isValid("O")
        expected = True
        self.assertEqual(expected,result)
if __name__ == '__main__':
    unittest.main()
