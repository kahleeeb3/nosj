import unittest
from nosj import *

# The test based on unittest module
class TestNosj(unittest.TestCase):
    def testInvalidInput(self):
        self.assertEqual(verifyInput('<<a :bs>>'), -1, "Didn't detect incorrect map") # whitespace in map
        self.assertEqual(verifyInput('<< a:bs>>'), -1, "Didn't detect incorrect map") # whitespace in map 1
        self.assertEqual(verifyInput('<< a:bs>>'), -1, "Didn't detect incorrect map") # whitespace in map 2
        self.assertEqual(verifyInput('<<a:bs >>'), -1, "Didn't detect incorrect map") # whitespace in map 3

    def testValidInput(self):
        # nums
        self.assertEqual(verifyInput('f12.32f'), 1, "Didn't detect as num") # correct num 1
        self.assertEqual(verifyInput('f-5678.0f'), 1, "Didn't detect as num") # correct num 2

        # simple string
        self.assertEqual(verifyInput('abcds'), 2, "Didn't detect as ss") # correct simple-string 1
        self.assertEqual(verifyInput('ef ghs'), 2, "Didn't detect as ss") # correct simple-string 2

        # complex string
        self.assertEqual(verifyInput('ab%2Ccd'), 3, "Didn't detect as cs") # correct complex-string 1
        self.assertEqual(verifyInput('ef%00gh'), 3, "Didn't detect as cs") # correct complex-string 2


        # maps
        self.assertEqual(verifyInput('      <<a:bs>>'), 4, "Didn't detect as map") # space before map
        self.assertEqual(verifyInput('<<a:bs>>      '), 4, "Didn't detect as map") # space after map
        self.assertEqual(verifyInput('<<x:abcds>>'), 4, "Didn't detect as map") # correct map 1
        self.assertEqual(verifyInput('<<x:abcds,y:f1.23f>>'), 4, "Didn't detect as map") # correct map 2
        self.assertEqual(verifyInput('<<x:<<y:f1.23f>>>>'), 4, "Didn't detect as map") # correct map 3
        # '<<x:abcds,y:f1.23f,z:<<a:bs,cds>>>>'

# run the test
unittest.main()