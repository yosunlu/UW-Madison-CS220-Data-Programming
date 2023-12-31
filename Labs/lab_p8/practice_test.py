#!/usr/bin/python
import os, json, math


REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats

PASS = "PASS"

TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool
TEXT_FORMAT_NAMEDTUPLE = "text namedtuple"  # question type when expected answer is a namedtuple
TEXT_FORMAT_UNORDERED_LIST = "text list_unordered"  # question type when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "text list_ordered"  # question type when the expected answer is a list where the order does matter
TEXT_FORMAT_ORDERED_LIST_NAMEDTUPLE = "text list_ordered namedtuple"  # question type when the expected answer is a list of namedtuples where the order does matter
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "text list_special_ordered"  # question type when the expected answer is a list where order does matter, but with possible ties. Elements are ordered according to values in special_ordered_json (with ties allowed)
TEXT_FORMAT_DICT = "text dict"  # question type when the expected answer is a dictionary


expected_json =    {"1": (TEXT_FORMAT_ORDERED_LIST, ['title', 'year', 'duration', 'genres', 'rating', 'directors', 'cast']),
                    "2": (TEXT_FORMAT_ORDERED_LIST, [['tt3104988',
                                                      '2018',
                                                      '120',
                                                      'Comedy, Drama, Romance',
                                                      '6.9',
                                                      'nm0160840',
                                                      'nm2090422, nm6525901, nm0000706, nm2110418, nm0523734'],
                                                     ['tt4846340',
                                                      '2016',
                                                      '127',
                                                      'Biography, Drama, History',
                                                      '7.8',
                                                      'nm0577647',
                                                      'nm0378245, nm0818055, nm1847117']]),
                    "3": (TEXT_FORMAT_ORDERED_LIST, [['tt3104988', 'Crazy Rich Asians'],
                                                    ['nm0160840', 'Jon M. Chu'],
                                                    ['nm2090422', 'Constance Wu'],
                                                    ['nm6525901', 'Henry Golding'],
                                                    ['nm0000706', 'Michelle Yeoh'],
                                                    ['nm2110418', 'Gemma Chan'],
                                                    ['nm0523734', 'Lisa Lu'],
                                                    ['tt4846340', 'Hidden Figures'],
                                                    ['nm0577647', 'Theodore Melfi'],
                                                    ['nm0378245', 'Taraji P. Henson'],
                                                    ['nm0818055', 'Octavia Spencer'],
                                                    ['nm1847117', 'Janelle Monáe']]),
                    "4": (TEXT_FORMAT_DICT, {'tt3104988': 'Crazy Rich Asians',
                                                    'nm0160840': 'Jon M. Chu',
                                                    'nm2090422': 'Constance Wu',
                                                    'nm6525901': 'Henry Golding',
                                                    'nm0000706': 'Michelle Yeoh',
                                                    'nm2110418': 'Gemma Chan',
                                                    'nm0523734': 'Lisa Lu',
                                                    'tt4846340': 'Hidden Figures',
                                                    'nm0577647': 'Theodore Melfi',
                                                    'nm0378245': 'Taraji P. Henson',
                                                    'nm0818055': 'Octavia Spencer',
                                                    'nm1847117': 'Janelle Monáe'}),
                    "5": (TEXT_FORMAT, 'Jon M. Chu'),
                    "6": (TEXT_FORMAT, 'Hidden Figures'),
                    "7-1": (TEXT_FORMAT_DICT, {'title': 'tt3104988',
                                                     'year': '2018',
                                                     'duration': '120',
                                                     'genres': 'Comedy, Drama, Romance',
                                                     'rating': '6.9',
                                                     'directors': 'nm0160840',
                                                     'cast': 'nm2090422, nm6525901, nm0000706, nm2110418, nm0523734'}),
                    "7-2": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'tt3104988',
                                                    'year': '2018',
                                                    'duration': '120',
                                                    'genres': 'Comedy, Drama, Romance',
                                                    'rating': '6.9',
                                                    'directors': 'nm0160840',
                                                    'cast': 'nm2090422, nm6525901, nm0000706, nm2110418, nm0523734'},
                                                    {'title': 'tt4846340',
                                                    'year': '2016',
                                                    'duration': '127',
                                                    'genres': 'Biography, Drama, History',
                                                    'rating': '7.8',
                                                    'directors': 'nm0577647',
                                                    'cast': 'nm0378245, nm0818055, nm1847117'}]),
                    "8": (TEXT_FORMAT, 'tt3104988'),
                    "9": (TEXT_FORMAT, '127'),
                    "10": (TEXT_FORMAT, 'Biography, Drama, History'),
                    "11": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'tt3104988',
                                                  'year': 2018,
                                                  'duration': 120,
                                                  'genres': 'Comedy, Drama, Romance',
                                                  'rating': 6.9,
                                                  'directors': 'nm0160840',
                                                  'cast': 'nm2090422, nm6525901, nm0000706, nm2110418, nm0523734'},
                                                 {'title': 'tt4846340',
                                                  'year': 2016,
                                                  'duration': 127,
                                                  'genres': 'Biography, Drama, History',
                                                  'rating': 7.8,
                                                  'directors': 'nm0577647',
                                                  'cast': 'nm0378245, nm0818055, nm1847117'}]),
                    "12": (TEXT_FORMAT, int),
                    "13": (TEXT_FORMAT, float),
                    "14": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'tt3104988',
                                                  'year': 2018,
                                                  'duration': 120,
                                                  'genres': ['Comedy', 'Drama', 'Romance'],
                                                  'rating': 6.9,
                                                  'directors': ['nm0160840'],
                                                  'cast': ['nm2090422', 'nm6525901', 'nm0000706', 'nm2110418', 'nm0523734']},
                                                 {'title': 'tt4846340',
                                                  'year': 2016,
                                                  'duration': 127,
                                                  'genres': ['Biography', 'Drama', 'History'],
                                                  'rating': 7.8,
                                                  'directors': ['nm0577647'],
                                                  'cast': ['nm0378245', 'nm0818055', 'nm1847117']}]),
                    "15": (TEXT_FORMAT_ORDERED_LIST, ['Biography', 'Drama', 'History']),
                    "16": (TEXT_FORMAT, 3),
                    "17-1": (TEXT_FORMAT, 'Hidden Figures'),
                    "17-2": (TEXT_FORMAT_ORDERED_LIST, ['Constance Wu', 'Henry Golding', 'Michelle Yeoh', 'Gemma Chan', 'Lisa Lu']),
                    "17-3": (TEXT_FORMAT_ORDERED_LIST, ['Jon M. Chu', 'Theodore Melfi']),
                    "18-1": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Crazy Rich Asians',
                                                  'year': 2018,
                                                  'duration': 120,
                                                  'genres': ['Comedy', 'Drama', 'Romance'],
                                                  'rating': 6.9,
                                                  'directors': ['nm0160840'],
                                                  'cast': ['nm2090422', 'nm6525901', 'nm0000706', 'nm2110418', 'nm0523734']},
                                                 {'title': 'Hidden Figures',
                                                  'year': 2016,
                                                  'duration': 127,
                                                  'genres': ['Biography', 'Drama', 'History'],
                                                  'rating': 7.8,
                                                  'directors': ['nm0577647'],
                                                  'cast': ['nm0378245', 'nm0818055', 'nm1847117']}]),
                    "18-2": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Crazy Rich Asians',
                                                  'year': 2018,
                                                  'duration': 120,
                                                  'genres': ['Comedy', 'Drama', 'Romance'],
                                                  'rating': 6.9,
                                                  'directors': ['Jon M. Chu'],
                                                  'cast': ['nm2090422', 'nm6525901', 'nm0000706', 'nm2110418', 'nm0523734']},
                                                 {'title': 'Hidden Figures',
                                                  'year': 2016,
                                                  'duration': 127,
                                                  'genres': ['Biography', 'Drama', 'History'],
                                                  'rating': 7.8,
                                                  'directors': ['Theodore Melfi'],
                                                  'cast': ['nm0378245', 'nm0818055', 'nm1847117']}]),
                    "18-3": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Crazy Rich Asians',
                                                  'year': 2018,
                                                  'duration': 120,
                                                  'genres': ['Comedy', 'Drama', 'Romance'],
                                                  'rating': 6.9,
                                                  'directors': ['Jon M. Chu'],
                                                  'cast': ['Constance Wu',
                                                   'Henry Golding',
                                                   'Michelle Yeoh',
                                                   'Gemma Chan',
                                                   'Lisa Lu']},
                                                 {'title': 'Hidden Figures',
                                                  'year': 2016,
                                                  'duration': 127,
                                                  'genres': ['Biography', 'Drama', 'History'],
                                                  'rating': 7.8,
                                                  'directors': ['Theodore Melfi'],
                                                  'cast': ['Taraji P. Henson', 'Octavia Spencer', 'Janelle Monáe']}]),
                    "19": (TEXT_FORMAT, 'Crazy Rich Asians'),
                    "20": (TEXT_FORMAT_ORDERED_LIST, ['Theodore Melfi'])
                   }

def check_cell(qnum, actual):
    format, expected = expected_json[qnum[1:]]
    try:
        if format == TEXT_FORMAT:
            return simple_compare(expected, actual)
        elif format == TEXT_FORMAT_UNORDERED_LIST:
            return list_compare_unordered(expected, actual)
        elif format == TEXT_FORMAT_ORDERED_LIST:
            return list_compare_ordered(expected, actual)
        elif format == TEXT_FORMAT_DICT:
            return dict_compare(expected, actual)
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

def namedtuple_compare(expected, actual):
    msg = PASS
    for field in expected._fields:
        val = simple_compare(getattr(expected, field), getattr(actual, field))
        if val != PASS:
            msg = "at attribute %s of namedtuple %s, " % (field, type(expected).__name__) + val
            return msg
    return msg


def list_compare_ordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    for i in range(len(expected)):
        if i >= len(actual):
            msg = "expected missing %s in %s" % (repr(expected[i]), obj)
            break
        if type(expected[i]) in [int, float, bool, str]:
            val = simple_compare(expected[i], actual[i])
        elif type(expected[i]) in [list]:
            val = list_compare_ordered(expected[i], actual[i], "sub" + obj)
        elif type(expected[i]) in [dict]:
            val = dict_compare(expected[i], actual[i])
        elif type(expected[i]).__name__ == obfuscate1():
            val = simple_compare(expected[i], actual[i])
        if val != PASS:
            msg = "at index %d of the %s, " % (i, obj) + val
            break
    if len(actual) > len(expected) and msg == PASS:
        msg = "found unexpected %s in %s" % (repr(actual[len(expected)]), obj)
    if len(expected) != len(actual):
        msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))

    if len(expected) > 0 and type(expected[0]) in [int, float, bool, str]:
        if msg != PASS and list_compare_unordered(expected, actual, obj) == PASS:
            try:
                msg = msg + " (list may not be ordered as required)"
            except:
                pass
    return msg


def list_compare_helper(larger, smaller):
    msg = PASS
    j = 0
    for i in range(len(larger)):
        if i == len(smaller):
            msg = "expected %s" % (repr(larger[i]))
            break
        found = False
        while not found:
            if j == len(smaller):
                val = simple_compare(larger[i], smaller[j - 1], False)
                break
            val = simple_compare(larger[i], smaller[j], False)
            j += 1
            if val == PASS:
                found = True
                break
        if not found:
            msg = val
            break
    return msg


def list_compare_unordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    try:
        sort_expected = sorted(expected)
        sort_actual = sorted(actual)
    except:
        msg = "unexpected datatype found in %s; expected entries of type %s" % (obj, obj, type(expected[0]).__name__)
        return msg

    if len(actual) == 0 and len(expected) > 0:
        msg = "in the %s, missing" % (obj) + expected[0]
    elif len(actual) > 0 and len(expected) > 0:
        val = simple_compare(sort_expected[0], sort_actual[0])
        if val.startswith("expected to find type"):
            msg = "in the %s, " % (obj) + simple_compare(sort_expected[0], sort_actual[0])
        else:
            if len(expected) > len(actual):
                msg = "in the %s, missing " % (obj) + list_compare_helper(sort_expected, sort_actual)
            elif len(expected) < len(actual):
                msg = "in the %s, found un" % (obj) + list_compare_helper(sort_actual, sort_expected)
            if len(expected) != len(actual):
                msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))
                return msg
            else:
                val = list_compare_helper(sort_expected, sort_actual)
                if val != PASS:
                    msg = "in the %s, missing " % (obj) + val + ", but found un" + list_compare_helper(sort_actual,
                                                                                               sort_expected)
    return msg

def list_compare_special_init(expected, special_order):
    real_expected = []
    for i in range(len(expected)):
        if real_expected == [] or special_order[i-1] != special_order[i]:
            real_expected.append([])
        real_expected[-1].append(expected[i])
    return real_expected


def list_compare_special(expected, actual, special_order):
    expected = list_compare_special_init(expected, special_order)
    msg = PASS
    expected_list = []
    for expected_item in expected:
        expected_list.extend(expected_item)
    val = list_compare_unordered(expected_list, actual)
    if val != PASS:
        msg = val
    else:
        i = 0
        for expected_item in expected:
            j = len(expected_item)
            actual_item = actual[i: i + j]
            val = list_compare_unordered(expected_item, actual_item)
            if val != PASS:
                if j == 1:
                    msg = "at index %d " % (i) + val
                else:
                    msg = "between indices %d and %d " % (i, i + j - 1) + val
                msg = msg + " (list may not be ordered as required)"
                break
            i += j

    return msg


def dict_compare(expected, actual, obj="dict"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    try:
        expected_keys = sorted(list(expected.keys()))
        actual_keys = sorted(list(actual.keys()))
    except:
        msg = "unexpected datatype found in keys of dict; expect a dict with keys of type %s" % (
            type(expected_keys[0]).__name__)
        return msg
    val = list_compare_unordered(expected_keys, actual_keys, "dict")
    if val != PASS:
        msg = "bad keys in %s: " % (obj) + val
    if msg == PASS:
        for key in expected:
            if expected[key] == None or type(expected[key]) in [int, float, bool, str]:
                val = simple_compare(expected[key], actual[key])
            elif type(expected[key]) in [list]:
                val = list_compare_ordered(expected[key], actual[key], "value")
            elif type(expected[key]) in [dict]:
                val = dict_compare(expected[key], actual[key], "sub" + obj)
            if val != PASS:
                msg = "incorrect val for key %s in %s: " % (repr(key), obj) + val
    return msg


def check(qnum, actual):
    msg = check_cell(qnum, actual)
    if msg == PASS:
        return True
    print("<b style='color: red;'>ERROR:</b> " + msg)
