#!/usr/bin/python

import os, json, math


REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats

PASS = "PASS"

TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool

expected_json =    {"1-1": (TEXT_FORMAT, '1804 New England hurricane'),
                    "1-2": (TEXT_FORMAT, '1806 Great Coastal hurricane'),
                    "1-3": (TEXT_FORMAT, 105),
                    "1-4": (TEXT_FORMAT, '1M'),
                    "2": (TEXT_FORMAT, 'Fiona'),
                    "3-1": (TEXT_FORMAT, '9'),
                    "3-2": (TEXT_FORMAT, '608'),
                    "3-3": (TEXT_FORMAT, '5309'),
                    "3-4": (TEXT_FORMAT, '867'),
                    "4-1": (TEXT_FORMAT, 'CS'),
                    "4-2": (TEXT_FORMAT, '220'),
                    "5-1": (TEXT_FORMAT, 'B'),
                    "5-2": (TEXT_FORMAT, 3.19),
                    "6": (TEXT_FORMAT, 9),
                    "7": (TEXT_FORMAT, 2022),
                    "8": (TEXT_FORMAT, 5),
                    "9": (TEXT_FORMAT, 13),
                    "10": (TEXT_FORMAT, 1979),
                    "11": (TEXT_FORMAT, 8),
                    "12": (TEXT_FORMAT, 325),
                    "13": (TEXT_FORMAT, 325),
                    "14": (TEXT_FORMAT, 1920),
                    "15": (TEXT_FORMAT, 99.44241316270566),
                    "16": (TEXT_FORMAT, 18),
                    "17": (TEXT_FORMAT, 40),
                    "18": (TEXT_FORMAT, 'Allen'),
                    "19": (TEXT_FORMAT, '1975 Tropical Depression Six'),
                    "20-1": (TEXT_FORMAT, 130),
                    "20-2": (TEXT_FORMAT, 294)}

def check_cell(qnum, actual):
    format, expected = expected_json[qnum[1:]]
    try:
        if format == TEXT_FORMAT:
            return simple_compare(expected, actual)
        else:
            if expected != actual:
                return "expected %s but found %s " % (repr(expected), repr(actual))
    except:
        if expected != actual:
            return "expected %s" % (repr(expected))
    return PASS


def simple_compare(expected, actual, complete_msg=True):
    msg = PASS
    if type(expected) == type:
        if expected != actual:
            if type(actual) == type:
                msg = "expected %s but found %s" % (expected.__name__, actual.__name__)
            else:
                msg = "expected %s but found %s" % (expected.__name__, repr(actual))
    elif type(expected) != type(actual) and not (type(expected) in [float, int] and type(actual) in [float, int]):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL):
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    else:
        if expected != actual:
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    return msg

def check(qnum, actual):
    msg = check_cell(qnum, actual)
    if msg == PASS:
        return True
    print("<b style='color: red;'>ERROR:</b> " + msg)
