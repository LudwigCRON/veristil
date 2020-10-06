#!/usr/bin/env python3
# coding: utf-8

import os
import unittest
from veristil.stil import TokenType
import veristil
from pprint import pprint


class TestTiming(unittest.TestCase):
    def test_tokenize_timing(self):
        expected_tokens = [
            (1, veristil.stil.TokenType.ANY, "Timing"),
            (1, veristil.stil.TokenType.STRING, "Param_Time_Set"),
            (1, veristil.stil.TokenType.BLOCK_START, None),
            (1, veristil.stil.TokenType.NEW_LINE, None),
            (2, veristil.stil.TokenType.ANY, "WaveformTable"),
            (2, veristil.stil.TokenType.STRING, "T1"),
            (2, veristil.stil.TokenType.BLOCK_START, None),
            (2, veristil.stil.TokenType.NEW_LINE, None),
            (3, veristil.stil.TokenType.ANY, "Period"),
            (3, veristil.stil.TokenType.MULTISTRING, None),
            (3, veristil.stil.TokenType.ANY, "100nS"),
            (3, veristil.stil.TokenType.MULTISTRING, None),
            (3, veristil.stil.TokenType.END_OF_INST, None),
            (3, veristil.stil.TokenType.NEW_LINE, None),
            (4, veristil.stil.TokenType.ANY, "Waveforms"),
            (4, veristil.stil.TokenType.BLOCK_START, None),
            (4, veristil.stil.TokenType.NEW_LINE, None),
            (5, veristil.stil.TokenType.NEW_LINE, None),
            (6, veristil.stil.TokenType.STRING, "Control_pins"),
            (6, veristil.stil.TokenType.BLOCK_START, None),
            (6, veristil.stil.TokenType.ANY, "0"),
            (6, veristil.stil.TokenType.BLOCK_START, None),
            (6, veristil.stil.TokenType.MULTISTRING, None),
            (6, veristil.stil.TokenType.ANY, "45nS"),
            (6, veristil.stil.TokenType.MULTISTRING, None),
            (6, veristil.stil.TokenType.ANY, "D"),
            (6, veristil.stil.TokenType.END_OF_INST, None),
            (6, veristil.stil.TokenType.BLOCK_END, None),
            (6, veristil.stil.TokenType.BLOCK_END, None),
            (6, veristil.stil.TokenType.NEW_LINE, None),
            (7, veristil.stil.TokenType.STRING, "Control_pins"),
            (7, veristil.stil.TokenType.BLOCK_START, None),
            (7, veristil.stil.TokenType.ANY, "1"),
            (7, veristil.stil.TokenType.BLOCK_START, None),
            (7, veristil.stil.TokenType.MULTISTRING, None),
            (7, veristil.stil.TokenType.ANY, "50nS"),
            (7, veristil.stil.TokenType.MULTISTRING, None),
            (7, veristil.stil.TokenType.ANY, "U"),
            (7, veristil.stil.TokenType.END_OF_INST, None),
            (7, veristil.stil.TokenType.BLOCK_END, None),
            (7, veristil.stil.TokenType.BLOCK_END, None),
            (7, veristil.stil.TokenType.NEW_LINE, None),
            (8, veristil.stil.TokenType.STRING, "Data_pins"),
            (8, veristil.stil.TokenType.BLOCK_START, None),
            (8, veristil.stil.TokenType.ANY, "0"),
            (8, veristil.stil.TokenType.BLOCK_START, None),
            (8, veristil.stil.TokenType.MULTISTRING, None),
            (8, veristil.stil.TokenType.ANY, "10ns"),
            (8, veristil.stil.TokenType.MULTISTRING, None),
            (8, veristil.stil.TokenType.ANY, "D"),
            (8, veristil.stil.TokenType.END_OF_INST, None),
            (8, veristil.stil.TokenType.MULTISTRING, None),
            (8, veristil.stil.TokenType.ANY, "70nS"),
            (8, veristil.stil.TokenType.MULTISTRING, None),
            (8, veristil.stil.TokenType.ANY, "U"),
            (8, veristil.stil.TokenType.END_OF_INST, None),
            (8, veristil.stil.TokenType.BLOCK_END, None),
            (8, veristil.stil.TokenType.BLOCK_END, None),
            (8, veristil.stil.TokenType.NEW_LINE, None),
            (9, veristil.stil.TokenType.STRING, "Data_pins"),
            (9, veristil.stil.TokenType.BLOCK_START, None),
            (9, veristil.stil.TokenType.ANY, "1"),
            (9, veristil.stil.TokenType.BLOCK_START, None),
            (9, veristil.stil.TokenType.MULTISTRING, None),
            (9, veristil.stil.TokenType.ANY, "15ns"),
            (9, veristil.stil.TokenType.MULTISTRING, None),
            (9, veristil.stil.TokenType.ANY, "U"),
            (9, veristil.stil.TokenType.END_OF_INST, None),
            (9, veristil.stil.TokenType.MULTISTRING, None),
            (9, veristil.stil.TokenType.ANY, "75nS"),
            (9, veristil.stil.TokenType.MULTISTRING, None),
            (9, veristil.stil.TokenType.ANY, "D"),
            (9, veristil.stil.TokenType.END_OF_INST, None),
            (9, veristil.stil.TokenType.BLOCK_END, None),
            (9, veristil.stil.TokenType.BLOCK_END, None),
            (9, veristil.stil.TokenType.NEW_LINE, None),
            (10, veristil.stil.TokenType.STRING, "Clock_pins"),
            (10, veristil.stil.TokenType.BLOCK_START, None),
            (10, veristil.stil.TokenType.ANY, "1"),
            (10, veristil.stil.TokenType.BLOCK_START, None),
            (10, veristil.stil.TokenType.MULTISTRING, None),
            (10, veristil.stil.TokenType.ANY, "15ns"),
            (10, veristil.stil.TokenType.MULTISTRING, None),
            (10, veristil.stil.TokenType.ANY, "U"),
            (10, veristil.stil.TokenType.END_OF_INST, None),
            (10, veristil.stil.TokenType.MULTISTRING, None),
            (10, veristil.stil.TokenType.ANY, "75nS"),
            (10, veristil.stil.TokenType.MULTISTRING, None),
            (10, veristil.stil.TokenType.ANY, "D"),
            (10, veristil.stil.TokenType.END_OF_INST, None),
            (10, veristil.stil.TokenType.BLOCK_END, None),
            (10, veristil.stil.TokenType.BLOCK_END, None),
            (10, veristil.stil.TokenType.NEW_LINE, None),
            (11, veristil.stil.TokenType.STRING, "Clock_pins"),
            (11, veristil.stil.TokenType.BLOCK_START, None),
            (11, veristil.stil.TokenType.ANY, "0"),
            (11, veristil.stil.TokenType.BLOCK_START, None),
            (11, veristil.stil.TokenType.MULTISTRING, None),
            (11, veristil.stil.TokenType.ANY, "15ns"),
            (11, veristil.stil.TokenType.MULTISTRING, None),
            (11, veristil.stil.TokenType.ANY, "D"),
            (11, veristil.stil.TokenType.END_OF_INST, None),
            (11, veristil.stil.TokenType.BLOCK_END, None),
            (11, veristil.stil.TokenType.BLOCK_END, None),
            (11, veristil.stil.TokenType.NEW_LINE, None),
            (12, veristil.stil.TokenType.BLOCK_END, None),
            (12, veristil.stil.TokenType.NEW_LINE, None),
            (13, veristil.stil.TokenType.BLOCK_END, None),
            (13, veristil.stil.TokenType.NEW_LINE, None),
            (14, veristil.stil.TokenType.BLOCK_END, None),
            (14, veristil.stil.TokenType.NEW_LINE, None),
            (-1, TokenType.EOF, None),
        ]
        tokens = list(
            veristil.stil.tokenizer(f"{os.getenv('TEST_DIR')}/stil_timing_ok.stil")
        )
        self.assertEqual(len(tokens), len(expected_tokens))
        self.assertEqual(tokens, expected_tokens)

    def test_parse_timing(self):
        db = veristil.stil.parse_stil(f"{os.getenv('TEST_DIR')}/stil_timing_ok.stil")
        s = db["timing"][0]
        self.assertEqual(s.name, "Param_Time_Set")
        pprint(s.waveformtables[0].waveforms)
        self.assertEqual(len(s.waveformtables), 1)
        wt = s.waveformtables[0]
        self.assertEqual(wt.name, "T1")
        self.assertAlmostEqual(wt.period, 1e-7)
        self.assertEqual(len(wt.waveforms), 6)

    def test_real_timing(self):
        db = veristil.stil.parse_stil(f"{os.getenv('TEST_DIR')}/real_pattern.stil")
        pprint(db["timing"])


if __name__ == "__main__":
    unittest.main()
