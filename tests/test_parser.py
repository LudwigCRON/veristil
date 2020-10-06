#!/usr/bin/env python3
# coding: utf-8

import unittest
import veristil
from pprint import pprint


class TestParser(unittest.TestCase):
    def test_signal(self):
        print(dir(veristil))
        tokens = list(veristil.tokenizer("./stil_signal_ok.stil"))
        pprint(tokens)


if __name__ == "__main__":
    unittest.main()
