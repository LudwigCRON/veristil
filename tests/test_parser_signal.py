#!/usr/bin/env python3
# coding: utf-8

import os
import unittest
from veristil.stil import TokenType
import veristil
from pprint import pprint


class TestSignal(unittest.TestCase):
    def test_tokenize_signal(self):
        expected_tokens = [
            (1, veristil.stil.TokenType.ANY, "Signals"),
            (1, veristil.stil.TokenType.BLOCK_START, None),
            (1, veristil.stil.TokenType.NEW_LINE, None),
            (2, veristil.stil.TokenType.STRING, "pc4"),
            (2, veristil.stil.TokenType.ANY, "InOut"),
            (2, veristil.stil.TokenType.END_OF_INST, None),
            (2, veristil.stil.TokenType.NEW_LINE, None),
            (3, veristil.stil.TokenType.ANY, "irq"),
            (3, veristil.stil.TokenType.ANY, "InOut"),
            (3, veristil.stil.TokenType.END_OF_INST, None),
            (3, veristil.stil.TokenType.NEW_LINE, None),
            (4, veristil.stil.TokenType.ANY, "scan0"),
            (4, veristil.stil.TokenType.ANY, "In"),
            (4, veristil.stil.TokenType.BLOCK_START, None),
            (4, veristil.stil.TokenType.ANY, "ScanIn"),
            (4, veristil.stil.TokenType.END_OF_INST, None),
            (4, veristil.stil.TokenType.BLOCK_END, None),
            (4, veristil.stil.TokenType.NEW_LINE, None),
            (5, veristil.stil.TokenType.BLOCK_END, None),
            (5, veristil.stil.TokenType.NEW_LINE, None),
            (6, veristil.stil.TokenType.ANY, "Signals"),
            (6, veristil.stil.TokenType.BLOCK_START, None),
            (6, veristil.stil.TokenType.STRING, "pc4"),
            (6, veristil.stil.TokenType.ANY, "InOut"),
            (6, veristil.stil.TokenType.END_OF_INST, None),
            (6, veristil.stil.TokenType.ANY, "irq"),
            (6, veristil.stil.TokenType.ANY, "Out"),
            (6, veristil.stil.TokenType.END_OF_INST, None),
            (6, veristil.stil.TokenType.ANY, "scan0"),
            (6, veristil.stil.TokenType.ANY, "In"),
            (6, veristil.stil.TokenType.BLOCK_START, None),
            (6, veristil.stil.TokenType.ANY, "ScanIn"),
            (6, veristil.stil.TokenType.END_OF_INST, None),
            (6, veristil.stil.TokenType.BLOCK_END, None),
            (6, veristil.stil.TokenType.NEW_LINE, None),
            (7, veristil.stil.TokenType.BLOCK_END, None),
            (7, veristil.stil.TokenType.NEW_LINE, None),
            (8, veristil.stil.TokenType.ANY, "Signals"),
            (8, veristil.stil.TokenType.BLOCK_START, None),
            (8, veristil.stil.TokenType.STRING, "pc4"),
            (8, veristil.stil.TokenType.ANY, "InOut"),
            (8, veristil.stil.TokenType.END_OF_INST, None),
            (8, veristil.stil.TokenType.ANY, "irq"),
            (8, veristil.stil.TokenType.ANY, "InOut"),
            (8, veristil.stil.TokenType.END_OF_INST, None),
            (8, veristil.stil.TokenType.ANY, "scan0"),
            (8, veristil.stil.TokenType.ANY, "In"),
            (8, veristil.stil.TokenType.BLOCK_START, None),
            (8, veristil.stil.TokenType.ANY, "ScanIn"),
            (8, veristil.stil.TokenType.END_OF_INST, None),
            (8, veristil.stil.TokenType.BLOCK_END, None),
            (8, veristil.stil.TokenType.BLOCK_END, None),
            (8, veristil.stil.TokenType.NEW_LINE, None),
            (-1, TokenType.EOF, None),
        ]
        tokens = list(
            veristil.stil.tokenizer(f"{os.getenv('TEST_DIR')}/stil_signal_ok.stil")
        )
        self.assertEqual(len(tokens), len(expected_tokens))
        self.assertEqual(tokens, expected_tokens)

    def test_parse_signal(self):
        db = veristil.stil.parse_stil(f"{os.getenv('TEST_DIR')}/stil_signal_ok.stil")
        self.assertEqual(len(db["signals"]), 9)
        s = db["signals"][0]
        self.assertEqual(s.name, "pc4")
        self.assertEqual(s.direction, veristil.stil.SignalDir.INOUT)
        self.assertEqual(s.attributes, [])
        s = db["signals"][4]
        self.assertEqual(s.name, "irq")
        self.assertEqual(s.direction, veristil.stil.SignalDir.OUT)
        self.assertEqual(s.attributes, [])
        s = db["signals"][8]
        self.assertEqual(s.name, "scan0")
        self.assertEqual(s.direction, veristil.stil.SignalDir.IN)
        self.assertEqual(s.attributes, ["ScanIn"])

    def test_real_signal(self):
        db = veristil.stil.parse_stil(f"{os.getenv('TEST_DIR')}/real_signal.stil")
        self.assertEqual(len(db["signals"]), 32)


if __name__ == "__main__":
    unittest.main()
