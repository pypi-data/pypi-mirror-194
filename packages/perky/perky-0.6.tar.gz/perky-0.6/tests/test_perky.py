#!/usr/bin/env python3

# use a crowbar on sys.path
# to let this script import perky
# without any additional work
assert __name__ == "__main__"
import os.path
from os.path import abspath, dirname
import sys
perky_dir = dirname(dirname(abspath(sys.argv[0])))
sys.path.insert(0, perky_dir)
os.chdir(perky_dir + "/tests")

import perky
import unittest


TEST_INPUT_TEXT = """

a = b
c = d
dict = {
    inner1=value1
      inner 2 = " value 2  "
      list = [

      a
        b

    c
        ]
}

list = [

    1
    2
    3
]

text = '''
    hello

    this is indented

    etc.
    '''

"""

TEST_INPUT_TEXT_TRIPLE_Q_ERROR = """

a = b
c = d
dict = {
    inner1=value1
      inner 2 = " value 2  "
      list = [

      a
        b

    c
        ]
}

list = [

    1
    2
    3
]

text = '''
    hello

    this is indented

    etc.
        '''

"""


TEST__PARSE_OUTPUT = {
                'a': 'b', 'c': 'd', 'dict': {'inner1': 'value1', 'inner 2': ' value 2  ', 'list': ['a', 'b', 'c']},
                'list': ['1', '2', '3'],
                'text': 'hello\n\nthis is indented\n\netc.'
               }


class TestParseMethods(unittest.TestCase):

    def test_parse_type(self):
        test = perky.loads(TEST_INPUT_TEXT)
        self.assertEqual(type(test), dict)

    def test_parse(self):
        test = perky.loads(TEST_INPUT_TEXT)
        self.assertEqual(test, TEST__PARSE_OUTPUT)

    def test_parse_no_input(self):
        with self.assertRaises(AttributeError):
            perky.loads(None)

    def test_parse_wrong_type_input(self):
        with self.assertRaises(AttributeError):
            perky.loads(3)

    def test_parse_unterminated_quoted_string(self):
        with self.assertRaises(SyntaxError):
            perky.loads("""
'quoted' = 'unterminated quoted string
""")

    def test_parse_triple_quote(self):
        d = perky.loads('''
a = """

    this is flush left
    note the          ^^
    intentional trailing whitespace!

      don't remove it, even though I
      know you want to.
    """

''')
        self.assertEqual(d['a'], "\nthis is flush left\nnote the          ^^\nintentional trailing whitespace!\n\n  don't remove it, even though I\n  know you want to.")

    def test_empty_dicts_and_lists(self):
        d = perky.loads('''
a = []
b = {}
c = [ ]
d = { }

''')
        self.assertEqual(d['a'], [])
        self.assertEqual(d['b'], {})
        self.assertEqual(d['c'], [])
        self.assertEqual(d['d'], {})

# TODO: add code changes to perky.py to raise an assertion error.
    def test_parse_trip_q_error(self):
        with self.assertRaises(perky.PerkyFormatError):
            perky.loads(TEST_INPUT_TEXT_TRIPLE_Q_ERROR)

    def test_parse_trip_repeated_key_error(self):
        # perky doesn't like it if you redefine the same key in a dict
        # twice in the same file.
        # note that perky explicitly doesn't complain if you
        # redefine a key in a different (as in, =include'd) file.
        # test_perky_include_nested tests redefining in different files.
        with self.assertRaises(perky.PerkyFormatError):
            perky.loads("a=3\na=5")

# TODO: check if there are any other formats that would cause a failure
    def test_read_file(self):
        test_input = perky.load("test_input.txt", encoding="utf-8")
        self.assertIsNotNone(self, test_input)

    def test_transform_dict(self):
        o = {'a': '3', 'b': '5.0', 'c': ['1', '2', 'None', '3'], 'd': {'e': 'f', 'g': 'True'}}
        schema = {'a': int, 'b': float, 'c': [perky.nullable(int)], 'd': {'e': str, 'g': perky.const}}
        test_func = perky.transform(o, schema)
        expected_dict = {'a': 3, 'b': 5.0, 'c': [1, 2, None, 3], 'd': {'e': 'f', 'g': True}}
        self.assertEqual(expected_dict, test_func)

    def test_transform_type_mismatch(self):
        o = {'a': '3', 'b': '5.0', 'c': ['1', '2', 'None', '3'], 'd': {'e': 'f', 'g': 'True'}}
        schema = [{'a': int, 'b': float, 'c': [perky.nullable(int)], 'd': {'e': str, 'g': perky.const}}]
        with self.assertRaises(perky.PerkyFormatError):
            perky.transform(o, schema)

    def test_transform_bad_obj(self):
        o2 = {'a': '44'}
        schema = [{'a': int, 'b': float, 'c': [perky.nullable(int)], 'd': {'e': str, 'g': perky.const}}]
        with self.assertRaises(perky.PerkyFormatError):
            perky.transform(o2, schema)

    def test_transform_none(self):
        o = None
        schema = {'a': int, 'b': float, 'c': [perky.nullable(int)], 'd': {'e': str, 'g': perky.const}}
        with self.assertRaises(perky.PerkyFormatError):
            perky.transform(o, schema)

    def test_perky_include_list(self):
        with perky.pushd("include_list"):
            root = perky.load("main.pky", root=[], pragmas={'include':perky.pragma_include()})
        self.assertEqual(root, list("abcd"))

    def test_perky_include_dict(self):
        with perky.pushd("include_dict"):
            root = perky.load("main.pky", pragmas={'include':perky.pragma_include()})
        self.assertEqual(root, dict(zip("abcd", "1234")))

    def test_perky_include_nested(self):
        with perky.pushd("include_nested"):
            root = perky.load("main.pky", pragmas={'include':perky.pragma_include()})
        self.assertEqual(root,
            {
                'a': '1',
                'b': {
                    'ba': '1',
                    'bb': '2',
                    'bc': '3',
                    'bd': '4',
                    'nested_dict': {
                        'x': '3',
                        'y': '2',
                        'z': ['1', '2', '3', '4']
                        },
                    'nested_list': ['a', 'b', 'c'],
                    },
                'c': '3',
                'd': '4'}
            )

    def test_perky_include_path(self):
        with perky.pushd("include_path"):
            root = perky.load("dir1/main.pky", pragmas={'include':perky.pragma_include( ['dir1', 'dir2'] )})
        self.assertEqual(root, dict(zip("abc", "345")))

    def test_perky_invalid_pragma(self):
        with self.assertRaises(perky.PerkyFormatError):
            root = perky.loads("a=b\n=include '''\nc=d\n", pragmas={'include':perky.pragma_include()})

    def test_perky_roundtrip(self):
        for i in range(1, 300):
            c = chr(i)
            if c.isspace():
                continue
            hex_digits = hex(i).partition("x")[2].rjust(4, "0")
            s = f"U+{hex_digits} {c}"

            d1 = {s:s}
            s1 = perky.dumps(d1)
            d2 = perky.loads(s1)
            s2 = perky.dumps(d2)
            self.assertEqual(d1, d2)
            self.assertEqual(s1, s2)

    def test_pushback_str_iterator(self):
        i = perky.pushback_str_iterator("abcde")
        strings = []
        strings.append(next(i)) # a
        strings.append(next(i)) # b
        i.push_c("X")
        strings.append(next(i)) # X
        strings.append(next(i)) # c
        i.push("YZ")
        for c in i:
            strings.append(c) # Y Z d e
        self.assertEqual("".join(strings), "abXcYZde")

        i = perky.pushback_str_iterator("abcde")
        i.push_c("X")
        i.push("nozzle")
        i.push(['Y', 'Z'])
        self.assertEqual(i.drain(), "YZnozzleXabcde")


if __name__ == '__main__':
    unittest.main()
