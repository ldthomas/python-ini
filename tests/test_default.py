import unittest
from python_ini.ini_file import IniFile


class TestGlobalSingle(unittest.TestCase):
    """Test the use of default values."""

    def test_default_1(self):
        '''Global default keys = multi.'''
        fname = 'tests/data/disjoint.ini'
        ini = IniFile('m')
        ini.parse(fname)
        value = ini.get_values('notkey', 'default-value')
        self.assertEqual(value, 'default-value')
        value = ini.get_values('notkey', [1, 2])
        self.assertEqual(value, [1, 2])

    def test_default_2(self):
        '''Global default keys - single.'''
        fname = 'tests/data/disjoint.ini'
        ini = IniFile()
        ini.parse(fname)
        value = ini.get_values('notkey', 'default-value')
        self.assertEqual(value, 'default-value')
        value = ini.get_values('notkey', [1, 2])
        self.assertEqual(value, [1, 2])
        ini = IniFile('m')
        ini.parse(fname)
        value = ini.get_values('notkey', 'default-value')
        self.assertEqual(value, 'default-value')
        value = ini.get_values('notkey', [1, 2])
        self.assertEqual(value, [1, 2])

    def test_default_3(self):
        '''No section name.'''
        fname = 'tests/data/disjoint.ini'
        ini = IniFile()
        ini.parse(fname)
        value = ini.get_section_values('nosection', 'nokey', 'default-value')
        self.assertEqual(value, 'default-value')
        value = ini.get_section_values('nosection', 'nokey', [1, 2])
        self.assertEqual(value, [1, 2])
        ini = IniFile('m')
        ini.parse(fname)
        value = ini.get_section_values('nosection', 'nokey', 'default-value')
        self.assertEqual(value, 'default-value')
        value = ini.get_section_values('nosection', 'nokey', [1, 2])
        self.assertEqual(value, [1, 2])

    def test_default_4(self):
        '''No section key name.'''
        fname = 'tests/data/disjoint.ini'
        ini = IniFile()
        ini.parse(fname)
        value = ini.get_section_values('_SECTION_', 'nokey', 'default-value')
        self.assertEqual(value, 'default-value')
        value = ini.get_section_values('_SECTION_', 'nokey', [1, 2])
        self.assertEqual(value, [1, 2])
        ini = IniFile('m')
        ini.parse(fname)
        value = ini.get_section_values('_SECTION_', 'nokey', 'default-value')
        self.assertEqual(value, 'default-value')
        value = ini.get_section_values('_SECTION_', 'nokey', [1, 2])
        self.assertEqual(value, [1, 2])


if __name__ == '__main__':
    unittest.main()
