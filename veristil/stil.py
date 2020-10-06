#!/usr/bin/env python3
# coding: utf-8

"""
    Toy STIL file parser
    -> use a parser generator for proper linting
    -> and error checking
"""

import logging
from enum import Enum

logger = logging.getLogger("stil")
logger.setLevel(logging.DEBUG)


class TokenType(Enum):
    BLOCK_NAME = 0
    BLOCK_START = 1
    BLOCK_END = 2
    STRING = 3
    END_OF_INST = 4
    EOF = 5
    NEW_LINE = 6
    ANY = 7
    ADD = 8
    ASSIGN = 9
    IGNORE = 10
    MULTISTRING = 11


class SignalDir(Enum):
    IN = 0
    OUT = 1
    INOUT = 2
    UNKNOWN = 3


class Signal(object):
    __slots__ = ["name", "direction", "attributes"]

    def __init__(self):
        self.name = None
        self.direction = SignalDir.UNKNOWN
        self.attributes = []

    def __str__(self):
        return f"Signal(name={self.name}, direction={self.direction}, attributes={self.attributes})"

    def __repr__(self):
        return str(self)


class SignalGroup(object):
    __slots__ = ["name", "signals"]

    def __init__(self):
        self.name = None
        self.signals = []

    def __str__(self):
        return f"SignalGroup(name={self.name}, signals={self.signals})"

    def __repr__(self):
        return str(self)


class Timing(object):
    __slots__ = ["name", "waveformtables"]

    def __init__(self):
        self.name = None
        self.waveformtables = []


class WaveformTable(object):
    __slots__ = ["name", "waveforms", "period"]

    def __init__(self):
        self.name = None
        self.waveforms = []
        self.period = None


class Waveform(object):
    __slots__ = ["name", "wave"]

    def __init__(self):
        self.name = None
        self.wave = []


def parse_time(s: str):
    print(f"parsing time [{s}]")
    num = float("0" + "".join([c for c in s if c in "0123456789."]))
    unit = "".join([c for c in s if c in "fpnumsFPNUMS"]).lower()
    mapping = {"fs": 1e-15, "ps": 1e-12, "ns": 1e-9, "us": 1e-6, "ms": 1e-3, "s": 1.0}
    return num * mapping.get(unit, 1e-9)


def tokenizer(filename: str):
    buf = []
    string_started = False
    mapping_table = {
        " ": TokenType.IGNORE,
        "\t": TokenType.IGNORE,
        "'": TokenType.MULTISTRING,
        ";": TokenType.END_OF_INST,
        "{": TokenType.BLOCK_START,
        "}": TokenType.BLOCK_END,
        "+": TokenType.ADD,
        "=": TokenType.ASSIGN,
    }
    with open(filename, "r+") as fp:
        for l, LINE in enumerate(fp):
            idx_cmt = LINE.find("//")
            line = LINE[:idx_cmt] if idx_cmt > -1 or LINE[-1] == "\n" else LINE
            for c in line:
                if c == '"':
                    string_started = not string_started
                    if not string_started:
                        yield (l + 1, TokenType.STRING, "".join(buf))
                        buf = []
                elif string_started:
                    buf.append(c)
                elif mapping_table.get(c, None) is not None:
                    if buf and not string_started:
                        yield (l + 1, TokenType.ANY, "".join(buf))
                    if mapping_table[c] != TokenType.IGNORE:
                        yield (l + 1, mapping_table[c], None)
                    buf = []
                else:
                    buf.append(c)
            if buf:
                yield (l + 1, TokenType.ANY, "".join(buf))
            yield (l + 1, TokenType.NEW_LINE, None)
    yield (-1, TokenType.EOF, None)


def parse_stil(filename: str):
    mapping_ctx = {"Signals": Signal, "SignalGroups": SignalGroup, "Timing": Timing}
    db = {"signals": [], "signalgroups": [], "timing": []}
    ctx = None
    block_level = 0
    multistring = False
    # waveforms
    wfc_name = None
    wfc_pattern = None
    waveform = None
    waveformtable = None
    is_waveform = False
    for line_number, type, token in tokenizer(filename):
        # debug only
        logger.debug(
            "%d %s %s %s",
            line_number,
            "".join(["\t"] * block_level),
            type,
            token if token is not None else "",
        )

        # context detection
        if ctx is None and type == TokenType.ANY and token in mapping_ctx.keys():
            ctx = mapping_ctx[token]()
            logger.debug(f"=========={ctx.__class__.__name__}===========")

        # sub fsm
        if isinstance(ctx, Signal) and block_level > 0:
            if ctx.name is None:
                if type in [TokenType.STRING, TokenType.ANY]:
                    ctx.name = token
                elif type == TokenType.BLOCK_START:
                    logger.error(
                        "Line %d: start a signal attribute block while the name of the signal is not given",
                        line_number,
                    )
            elif type == TokenType.ANY and ctx.direction == SignalDir.UNKNOWN:
                if not token in "InOut":
                    logger.error(
                        "Line %d: expect a direction after the signal name '%s'",
                        line_number,
                        ctx.name,
                    )
                else:
                    ctx.direction = (
                        SignalDir.IN
                        if token == "In"
                        else SignalDir.OUT
                        if token == "Out"
                        else SignalDir.INOUT
                    )
            elif type == TokenType.ANY:
                ctx.attributes.append(token)
            elif type == TokenType.END_OF_INST and block_level == 1:
                db["signals"].append(ctx)
                ctx = Signal()
            elif type == TokenType.BLOCK_END and block_level == 2:
                db["signals"].append(ctx)
                ctx = Signal()

        elif isinstance(ctx, SignalGroup) and block_level > 0:
            if ctx.name is None:
                if type in [TokenType.STRING, TokenType.ANY]:
                    ctx.name = token
                elif type == TokenType.BLOCK_START:
                    logger.error(
                        "Line %d: start a signalgroup while the name of the signal is not given",
                        line_number,
                    )
            elif multistring and type in [TokenType.STRING, TokenType.ANY]:
                ctx.signals.append(token)
            elif type == TokenType.END_OF_INST and block_level == 1:
                db["signalgroups"].append(ctx)
                ctx = SignalGroup()
            elif type == TokenType.BLOCK_END and block_level == 2:
                db["signalgroups"].append(ctx)
                ctx = SignalGroup()

            if type == TokenType.MULTISTRING:
                multistring = not multistring

        elif isinstance(ctx, Timing) and block_level >= 0:
            if block_level == 0 and type in [TokenType.STRING, TokenType.ANY]:
                if token != "Timing":
                    ctx.name = token
            if waveformtable is None and token == "WaveformTable":
                waveformtable = WaveformTable()
                is_waveform = False
            elif waveformtable and waveformtable.name is None and block_level == 1:
                if type in [TokenType.STRING, TokenType.ANY]:
                    waveformtable.name = token
            elif waveformtable and waveformtable.name and not is_waveform:
                if type in [TokenType.STRING, TokenType.ANY]:
                    if token == "Waveforms":
                        is_waveform = True
                        waveform = Waveform()
                    elif block_level == 2:
                        waveformtable.period = parse_time(token)
            elif is_waveform and block_level > 2:
                if block_level == 3 and type in [TokenType.STRING, TokenType.ANY]:
                    waveform.name = token
                elif block_level == 3 and type == TokenType.BLOCK_END:
                    waveformtable.waveforms.append(waveform)
                    waveform = Waveform()
                elif block_level == 4 and type in [TokenType.STRING, TokenType.ANY]:
                    wfc_name = token
                    wfc_pattern = []
                elif block_level == 5 and type in [TokenType.STRING, TokenType.ANY]:
                    wfc_pattern.append(token)
                elif block_level == 5 and type == TokenType.BLOCK_END:
                    waveform.wave.append(
                        (
                            wfc_name,
                            zip(
                                *[
                                    [parse_time(p) for p in wfc_pattern[0::2]],
                                    wfc_pattern[1::2],
                                ]
                            ),
                        )
                    )
            elif block_level == 3 and type == TokenType.BLOCK_END:
                is_waveform = False
            elif block_level == 2 and type == TokenType.BLOCK_END:
                ctx.waveformtables.append(waveformtable)
                waveformtable = None

        # update hierarchy level
        if type == TokenType.BLOCK_START:
            block_level += 1
        elif type == TokenType.BLOCK_END:
            block_level -= 1
            if block_level < 0:
                logger.error("Line %d: missing '{' detected", line_number)

        # dispatch the ctx obj
        if block_level == 0 and ctx is not None and type == TokenType.BLOCK_END:
            logger.debug("==========END================")
            if isinstance(ctx, Signal) and ctx.name is not None:
                db["signals"].append(ctx)
            elif isinstance(ctx, SignalGroup) and ctx.name is not None:
                db["signalgroups"].append(ctx)
            elif isinstance(ctx, Timing):
                db["timing"].append(ctx)
            ctx = None
    return db


# timing block
# waveform table
# dc levels
# pattern block
# pattern burst
# pattern exec
