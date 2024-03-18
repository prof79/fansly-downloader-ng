"""Cryptography Tests"""


import sys
import unittest

from pathlib import Path

sys.path.append(str(Path(__file__).parent.absolute().parent))
from api import FanslyApi


class CryptoTests(unittest.TestCase):

    def test_cyrb53(self):

        cases = [
            ('a', 0, 7929297801672961),
            ('b', 0, 8684336938537663),
            ('revenge', 0, 4051478007546757),
            ('revenue', 0, 8309097637345594),
            ('revenue', 1, 8697026808958300),
            ('revenue', 2, 2021074995066978),
            ('revenue', 3, 4747903550515895),
        ]

        for case in cases:
            result = FanslyApi.cyrb53(case[0], case[1])
            self.assertEqual(result, case[2], "Digest doesn't match")


    def test_imul32(self):

        cases = [
            (-559038834, 2654435761, -1447829970),
            (1103547958, 1597334677, -1401873042),
            (3294967296, 1337, -1265170944),
        ]

        for case in cases:
            result = FanslyApi.imul32(case[0], case[1])
            self.assertEqual(result, case[2], f"{case[0]} * {case[1]} should be {case[2]}, is {result}")



if __name__ == '__main__':
    unittest.main()
