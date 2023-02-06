import unittest
from python_ini.ini_file import IniFile


class TestStrings(unittest.TestCase):
    """Test string values."""

    def test_string_1(self):
        '''Bad string.'''
        fname = 'tests/data/interior_quotes.ini'
        ini = IniFile()
        ini.parse(fname)
        self.assertTrue(ini.errors)
        display = ini.display_errors()
        # print(display)
        self.assertTrue('bad key/value' in display)
        self.assertTrue('bad section' in display)

    def test_string_2(self):
        '''Bad string with good key/value line.'''
        fname = 'tests/data/interior_quotes.ini'
        ini = IniFile()
        ini.parse(fname)
        self.assertTrue(ini.errors)
        value = ini.get_values('key')
        self.assertEqual(value, 'value')


if __name__ == '__main__':
    unittest.main()
