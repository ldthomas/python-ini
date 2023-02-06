import unittest
import re
from python_ini.ini_file import IniFile


class TestHex(unittest.TestCase):
    """Test hexadecimal and Unicode values."""

    def test_hex_1(self):
        '''Good and Bad single hex values.'''
        ini_str = '''good = \\x00, \\x09 \\xff
one_bad = \\x00, \\xfg \\x10
all_bad = \\xxy, \\xyz \\xfy
bad = \\xa
'''
        ini = IniFile()
        ini.parse(fstr=ini_str)
        self.assertTrue(ini.errors)
        display = ini.display_errors()
        # print()
        # print(display)
        good = ini.get_values('good')
        bad = ini.get_values('one_bad')
        found = re.search(r'line: 2.*char code\(103\)', display)
        self.assertTrue(found)
        found = re.search(r'line: 3.*char code\(120\)', display)
        self.assertTrue(found)
        found = re.search(r'line: 4.*char code\(10\)', display)
        self.assertTrue(found)
        self.assertEqual(ord(good), 0xff)
        self.assertEqual(bad, None)

    def test_hex_2(self):
        '''Good and Bad multi-value hex values.'''
        ini_str = '''good = \\x00, \\x09 \\xff
one_bad = \\x00, \\xfg \\x10
all_bad = \\xxy, \\xyz \\xfy
bad = \\xa
'''
        ini = IniFile('m')
        ini.parse(fstr=ini_str)
        self.assertTrue(ini.errors)
        display = ini.display_errors()
        # print()
        # print(display)
        good = ini.get_values('good')
        self.assertIn('line: 2', display)
        self.assertIn('char code(103)', display)
        self.assertIn('line: 3', display)
        self.assertIn('char code(120)', display)
        self.assertIn('\x00', good)
        self.assertIn('\x09', good)
        self.assertIn('\xff', good)

    def test_hex_3(self):
        '''Good and Bad Unicode-16 single values.'''
        ini_str = '''good = \\u0000, \\u0009 \\ud7ff
one_bad = \\u0000, \\u0009 \\ud7fg
surrogate = \\ud800
'''
        ini = IniFile('s')
        ini.parse(fstr=ini_str)
        self.assertTrue(ini.errors)
        display = ini.display_errors()
        # print()
        # print(display)
        good = ini.get_values('good')
        self.assertEqual(ord(good), 0xd7ff)
        bad = ini.get_values('one_bad')
        self.assertFalse(bad)
        found = re.search(
            r'line: 2.*Unicode-16 value.*invalid hex digit.*char code\(103\)',
            display)
        self.assertTrue(found)
        found = re.search(
            r'line: 3.*Unicode-16 value.*surrogates not allowed.*0xd800',
            display)
        self.assertTrue(found)

    def test_hex_4(self):
        '''Good and Bad Unicode-16 multi values.'''
        ini_str = '''good = \\u0000, \\u0009 \\ud7ff
one_bad = \\u0000, \\u0009 \\ud7fg
surrogate = \\ud800
'''
        ini = IniFile('m')
        ini.parse(fstr=ini_str)
        self.assertTrue(ini.errors)
        display = ini.display_errors()
        # print()
        # print(display)
        good = ini.get_values('good')
        self.assertIn('\u0000', good)
        self.assertIn('\u0009', good)
        self.assertIn('\ud7ff', good)
        bad = ini.get_values('one_bad')
        self.assertFalse(bad)
        found = re.search(
            r'line: 2.*Unicode-16 value.*invalid hex digit.*char code\(103\)',
            display)
        self.assertTrue(found)
        found = re.search(
            r'line: 3.*Unicode-16 value.*surrogates not allowed.*0xd800',
            display)
        self.assertTrue(found)

    def test_hex_5(self):
        '''Good and Bad Unicode-32 single values.'''
        ini_str = '''good = \\U00000000, \\U00000009 \\U0010ffff
one_bad = \\U00000000, \\U00000009 \\U0000d7fg
surrogate = \\U0000d800
range = \\U00110000
'''
        ini = IniFile('s')
        ini.parse(fstr=ini_str)
        self.assertTrue(ini.errors)
        display = ini.display_errors()
        # print()
        # print(display)
        good = ini.get_values('good')
        # print('good = ', end='')
        # print(good)
        self.assertEqual(ord(good), 0x10ffff)
        bad = ini.get_values('surrogate')
        self.assertFalse(bad)
        bad = ini.get_values('range')
        # print('bad', end=' = ')
        # print(bad)
        self.assertFalse(bad)
        found = re.search(
            r'line: 2.*Unicode-32 value.*invalid hex digit.*char code\(103\)',
            display)
        self.assertTrue(found)
        found = re.search(
            r'line: 3.*Unicode-32 value.*surrogates not allowed.*0xd800',
            display)
        self.assertTrue(found)
        found = re.search(
            r'line: 4.*Unicode-32 value.*value out of range.*0x110000',
            display)
        self.assertTrue(found)

    def test_hex_6(self):
        '''Bad escaped characters.'''
        ini_str = '''escaped = \\00000000
bad = \\U00000000, \\X00000009 \\U0000d7fg
'''
        ini = IniFile('s')
        ini.parse(fstr=ini_str)
        self.assertTrue(ini.errors)
        display = ini.display_errors()
        # print()
        # print(display)
        found = re.search(
            r'line: 1.*unrecognized escaped character.*char code c\(48\)',
            display)
        self.assertTrue(found)
        found = re.search(
            r'line: 2.*unrecognized escaped character.*char code c\(88\)',
            display)
        self.assertTrue(found)


if __name__ == '__main__':
    unittest.main()
