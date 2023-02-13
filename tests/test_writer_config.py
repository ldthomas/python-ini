import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
import unittest
from python_ini.ini_writer import IniWriter
from python_ini.ini_file import IniFile


def make_ini(w):
    w.comment()
    w.comment('global section')
    w.key('aA0!$%()*+-.<>?@^_{|}~', [1, 2, 3], 'all key chars')
    w.key('floats', [1.0, -.3, -.3e2], 'floating point numbers')
    w.key('booleans', [True, False, None], 'boolean values')
    w.key('strings', ['abc', 'a\\bc', "a\\'"], 'some string values')
    w.comment()
    w.comment('start a new section')
    w.section('zZ9!$%()*+-.<>?@^_{|}~', 'odd section name')
    w.key('aA0!$%()*+-.<>?@^_{|}~', [1, 2, 3], 'all key chars')
    w.key('floats', [1.0, -.3, -.3e2], 'floating point numbers')
    w.key('booleans', [True, False, None], 'boolean values')
    w.key('strings', ['abc', 'a\\\\b', "a\\'"], 'some string values')


class TestConfig(unittest.TestCase):
    """Test all configurable options."""

    def test_delimiters_1(self):
        '''Default delimiters.'''
        w = IniWriter()
        make_ini(w)
        file = w.to_string()
        # print()
        # print(file)
        ini = IniFile('m')
        ini.parse(fstr=file)
        self.assertEqual(ini.errors, None)
        self.assertIn('; global section', file)
        self.assertIn('floats = ', file)
        self.assertIn('true, false, none', file)
        self.assertIn('        ; all key chars', file)
        s = ini.get_values('strings')
        # print(s)
        self.assertEqual(s[1], 'a c')
        self.assertEqual(s[2], "a'")

    def test_delimiters_2(self):
        '''#, : and space delimiters.'''
        w = IniWriter()
        w.delimiters('#', ':', ' ')
        make_ini(w)
        file = w.to_string()
        # print()
        # print(file)
        ini = IniFile('m')
        ini.parse(fstr=file)
        self.assertEqual(ini.errors, None)
        self.assertIn('# global section', file)
        self.assertIn('floats: ', file)
        self.assertIn('true false none', file)
        self.assertIn('        # all key chars', file)

    def test_delimiters_3(self):
        '''#, space and space delimiters.'''
        w = IniWriter()
        w.delimiters('#', ' ', ' ')
        make_ini(w)
        file = w.to_string()
        # print()
        # print(file)
        ini = IniFile('m')
        ini.parse(fstr=file)
        self.assertEqual(ini.errors, None)
        self.assertIn('# global section', file)
        self.assertIn('floats 1', file)
        self.assertIn('true false none', file)
        self.assertIn('        # all key chars', file)

    def test_booleans_1(self):
        '''Cap values for true, false, and none.'''
        w = IniWriter()
        w.booleans('TRUE', 'OFF', 'NULL')
        make_ini(w)
        file = w.to_string()
        # print()
        # print(file)
        ini = IniFile('m')
        ini.parse(fstr=file)
        self.assertEqual(ini.errors, None)
        self.assertIn('TRUE, OFF, NULL', file)

    def test_booleans_2(self):
        '''Mixed cap values for true, false, and none.'''
        w = IniWriter()
        w.booleans('YeS', 'nO', 'vOiD')
        make_ini(w)
        file = w.to_string()
        # print()
        # print(file)
        ini = IniFile('m')
        ini.parse(fstr=file)
        self.assertEqual(ini.errors, None)
        self.assertIn('YeS, nO, vOiD', file)

    def test_booleans_3(self):
        '''Mixed cap values for true, false, and none.'''
        w = IniWriter()
        w.booleans('True', 'False', 'None')
        make_ini(w)
        file = w.to_string()
        # print()
        # print(file)
        ini = IniFile('m')
        ini.parse(fstr=file)
        self.assertEqual(ini.errors, None)
        self.assertIn('True, False, None', file)

    def test_comment_tab_1(self):
        '''Mixed cap values for true, false, and none.'''
        w = IniWriter()
        make_ini(w)
        file = w.to_string()
        # print()
        # print(file)
        ini = IniFile('m')
        ini.parse(fstr=file)
        self.assertEqual(ini.errors, None)
        self.assertIn('        ; all key chars', file)
        w.clear()
        w.comment_tab(39)
        make_ini(w)
        file = w.to_string()
        ini.parse(fstr=file)
        # print(file)
        self.assertIn('       ; all key chars', file)
        w.clear()
        w.comment_tab(30)
        make_ini(w)
        file = w.to_string()
        ini.parse(fstr=file)
        # print(file)
        self.assertIn('                              ; all key chars', file)
        w.clear()
        w.comment_tab(0)
        make_ini(w)
        ini.parse(fstr=file)
        file = w.to_string()
        # print(file)
        self.assertIn('\n; all key chars', file)

    def test_write(self):
        '''Test writing to a file.'''
        fname = 'tests/data/temp.ini'
        w = IniWriter()
        ini = IniFile('m')
        make_ini(w)
        w.write(fname)
        # print()
        # print(file)
        ini.parse(fname)
        self.assertEqual(ini.errors, None)
        os.remove(fname)


if __name__ == '__main__':
    unittest.main()
