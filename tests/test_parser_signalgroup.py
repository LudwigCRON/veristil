#!/usr/bin/env python3
# coding: utf-8

import os
import unittest
from veristil.stil import TokenType
import veristil
from pprint import pprint


class TestSignalGroup(unittest.TestCase):
    def test_tokenize_signalgroup(self):
        expected_tokens = [
            (1, veristil.stil.TokenType.ANY, "SignalGroups"),
            (1, veristil.stil.TokenType.BLOCK_START, None),
            (1, veristil.stil.TokenType.NEW_LINE, None),
            (2, veristil.stil.TokenType.STRING, "porta"),
            (2, veristil.stil.TokenType.ASSIGN, None),
            (2, veristil.stil.TokenType.MULTISTRING, None),
            (2, veristil.stil.TokenType.STRING, "pa7"),
            (2, veristil.stil.TokenType.ADD, None),
            (2, veristil.stil.TokenType.STRING, "pa6"),
            (2, veristil.stil.TokenType.ADD, None),
            (2, veristil.stil.TokenType.STRING, "pa5"),
            (2, veristil.stil.TokenType.ADD, None),
            (2, veristil.stil.TokenType.STRING, "pa4"),
            (2, veristil.stil.TokenType.ADD, None),
            (2, veristil.stil.TokenType.STRING, "pa3"),
            (2, veristil.stil.TokenType.ADD, None),
            (2, veristil.stil.TokenType.STRING, "pa2"),
            (2, veristil.stil.TokenType.ADD, None),
            (2, veristil.stil.TokenType.STRING, "pa1"),
            (2, veristil.stil.TokenType.NEW_LINE, None),
            (3, veristil.stil.TokenType.ADD, None),
            (3, veristil.stil.TokenType.STRING, "pa0"),
            (3, veristil.stil.TokenType.MULTISTRING, None),
            (3, veristil.stil.TokenType.END_OF_INST, None),
            (3, veristil.stil.TokenType.NEW_LINE, None),
            (4, veristil.stil.TokenType.STRING, "portb"),
            (4, veristil.stil.TokenType.ASSIGN, None),
            (4, veristil.stil.TokenType.MULTISTRING, None),
            (4, veristil.stil.TokenType.STRING, "pb7"),
            (4, veristil.stil.TokenType.ADD, None),
            (4, veristil.stil.TokenType.STRING, "pb6"),
            (4, veristil.stil.TokenType.ADD, None),
            (4, veristil.stil.TokenType.STRING, "pb5"),
            (4, veristil.stil.TokenType.ADD, None),
            (4, veristil.stil.TokenType.STRING, "pb4"),
            (4, veristil.stil.TokenType.ADD, None),
            (4, veristil.stil.TokenType.STRING, "pb3"),
            (4, veristil.stil.TokenType.ADD, None),
            (4, veristil.stil.TokenType.STRING, "pb2"),
            (4, veristil.stil.TokenType.ADD, None),
            (4, veristil.stil.TokenType.STRING, "pb1"),
            (4, veristil.stil.TokenType.ADD, None),
            (4, veristil.stil.TokenType.STRING, "pb0"),
            (4, veristil.stil.TokenType.MULTISTRING, None),
            (4, veristil.stil.TokenType.END_OF_INST, None),
            (4, veristil.stil.TokenType.NEW_LINE, None),
            (5, veristil.stil.TokenType.ANY, "all"),
            (5, veristil.stil.TokenType.ASSIGN, None),
            (5, veristil.stil.TokenType.MULTISTRING, None),
            (5, veristil.stil.TokenType.ANY, "porta"),
            (5, veristil.stil.TokenType.ADD, None),
            (5, veristil.stil.TokenType.ANY, "portb"),
            (5, veristil.stil.TokenType.MULTISTRING, None),
            (5, veristil.stil.TokenType.END_OF_INST, None),
            (5, veristil.stil.TokenType.NEW_LINE, None),
            (6, veristil.stil.TokenType.ANY, "A"),
            (6, veristil.stil.TokenType.ASSIGN, None),
            (6, veristil.stil.TokenType.MULTISTRING, None),
            (6, veristil.stil.TokenType.ANY, "pa0"),
            (6, veristil.stil.TokenType.ADD, None),
            (6, veristil.stil.TokenType.ANY, "pa1"),
            (6, veristil.stil.TokenType.ADD, None),
            (6, veristil.stil.TokenType.ANY, "pa2"),
            (6, veristil.stil.TokenType.ADD, None),
            (6, veristil.stil.TokenType.ANY, "pa3"),
            (6, veristil.stil.TokenType.MULTISTRING, None),
            (6, veristil.stil.TokenType.BLOCK_START, None),
            (6, veristil.stil.TokenType.NEW_LINE, None),
            (7, veristil.stil.TokenType.ANY, "WFCMAP"),
            (7, veristil.stil.TokenType.BLOCK_START, None),
            (7, veristil.stil.TokenType.NEW_LINE, None),
            (8, veristil.stil.TokenType.ANY, "z->x"),
            (8, veristil.stil.TokenType.END_OF_INST, None),
            (8, veristil.stil.TokenType.NEW_LINE, None),
            (9, veristil.stil.TokenType.ANY, "01->x"),
            (9, veristil.stil.TokenType.END_OF_INST, None),
            (9, veristil.stil.TokenType.NEW_LINE, None),
            (10, veristil.stil.TokenType.BLOCK_END, None),
            (10, veristil.stil.TokenType.NEW_LINE, None),
            (11, veristil.stil.TokenType.BLOCK_END, None),
            (11, veristil.stil.TokenType.NEW_LINE, None),
            (12, veristil.stil.TokenType.BLOCK_END, None),
            (12, veristil.stil.TokenType.NEW_LINE, None),
            (-1, TokenType.EOF, None),
        ]
        tokens = list(
            veristil.stil.tokenizer(f"{os.getenv('TEST_DIR')}/stil_signal_group_ok.stil")
        )
        self.assertEqual(len(tokens), len(expected_tokens))
        self.assertEqual(tokens, expected_tokens)

    def test_parse_signalgroup(self):
        db = veristil.stil.parse_stil(f"{os.getenv('TEST_DIR')}/stil_signal_group_ok.stil")
        self.assertEqual(len(db["signalgroups"]), 4)
        s = db["signalgroups"][0]
        self.assertEqual(s.name, "porta")
        self.assertEqual(
            s.signals, ["pa7", "pa6", "pa5", "pa4", "pa3", "pa2", "pa1", "pa0"]
        )
        s = db["signalgroups"][1]
        self.assertEqual(s.name, "portb")
        self.assertEqual(
            s.signals, ["pb7", "pb6", "pb5", "pb4", "pb3", "pb2", "pb1", "pb0"]
        )
        s = db["signalgroups"][2]
        self.assertEqual(s.name, "all")
        self.assertEqual(s.signals, ["porta", "portb"])
        s = db["signalgroups"][3]
        self.assertEqual(s.name, "A")
        self.assertEqual(s.signals, ["pa0", "pa1", "pa2", "pa3"])

    def test_real_signalgroup(self):
        db = veristil.stil.parse_stil(f"{os.getenv('TEST_DIR')}/real_signal.stil")
        self.assertEqual(len(db["signalgroups"]), 8)


if __name__ == "__main__":
    unittest.main()
