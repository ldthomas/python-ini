import unittest
from python_ini.ini_file import IniFile


class TestGlobalSingle(unittest.TestCase):
    """Test parsing disjoint sections and keys in multi-value mode."""

    def test_multi_1(self):
        '''True flags in multi-value mode - input file name'''
        fname = 'tests/data/true_flag_globals.ini'
        # file name and values parameters are positional
        ini = IniFile('m')
        ini.parse(fname)
        keys = ini.get_keys()
        for key in keys:
            value = ini.get_values(key)
            self.assertEqual(value, [True])

    def test_multi_2(self):
        '''True flags in multi-value mode - input file handle'''
        fname = 'tests/data/true_flag_globals.ini'
        with open(fname, 'r') as fd:
            # file name and values parameters are no longer positional
            ini = IniFile('m')
            ini.parse(fhandle=fd)
            keys = ini.get_keys()
            for key in keys:
                value = ini.get_values(key)
                self.assertEqual(value, [True])

    def test_multi_3(self):
        '''True flags in multi-value mode - input string'''
        fname = 'tests/data/true_flag_globals.ini'
        with open(fname, 'r') as fd:
            input = fd.read()
            # file name and values parameters are no longer positional
            ini = IniFile('m')
            ini.parse(fstr=input)
            keys = ini.get_keys()
            for key in keys:
                value = ini.get_values(key)
                self.assertEqual(value, [True])

    def test_multi_4(self):
        '''Global, disjoint sections and disjoint keys'''
        fname = 'tests/data/disjoint.ini'
        ini = IniFile('m')
        ini.parse(fname)
        # test the global key
        keys = ini.get_keys()
        values = ini.get_values(keys[0])
        self.assertEqual(values, [1, 2, 'three'])
        sections = ini.get_sections()
        # test the first section
        keys = ini.get_section_keys(sections[0])
        values = ini.get_section_values(sections[0], keys[0])
        self.assertEqual(values, [1, 2, None])
        values = ini.get_section_values(sections[0], keys[1])
        self.assertEqual(values, [2, 3])
        values = ini.get_section_values(sections[0], keys[2])
        self.assertEqual(values, [3, 4])
        values = ini.get_section_values(sections[0], keys[3])
        self.assertEqual(values, [4, 5])
        # test the second section
        keys = ini.get_section_keys(sections[1])
        values = ini.get_section_values(sections[1], keys[0])
        self.assertEqual(values, [10, True, 50])
        values = ini.get_section_values(sections[1], keys[1])
        self.assertEqual(values, [20, False])
        values = ini.get_section_values(sections[1], keys[2])
        self.assertEqual(values, [30, 40])
        values = ini.get_section_values(sections[1], keys[3])
        self.assertEqual(values, [40, 50])


if __name__ == '__main__':
    unittest.main()
