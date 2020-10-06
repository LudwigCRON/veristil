#!/usr/bin/env python3
# coding: utf-8

from enum import Enum


class TokenType(Enum):
    BLOCK_NAME
    BLOCK_START
    BLOCK_END
    STRING
    END_OF_INST
    EOF


def tokenizer(filename: str):
    buf = []
    with open(filename, "r+") as fp:
        for LINE in fp:
            for c in LINE:
                if c in [" ", "\t", "n"]:
                    yield (TokenType.STRING, "".join(buf))
                    buf = []
                elif c in [";"]:
                    yield (TokenType.END_OF_INST,)
                elif c in ["{"]:
                    yield (TokenType.BLOCK_START,)
                elif c in ["}"]:
                    yield (TokenType.BLOCK_START,)
                else:
                    buf.append(c)
    return (TokenType.EOF,)


# signal
# timing block
# waveform table
# dc levels
# pattern block
# signal group
# pattern burst
# pattern exec
