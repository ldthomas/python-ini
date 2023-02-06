import unittest
from python_ini.ini_file import IniFile


def ini_data(fname):
    with open(fname, 'r') as fd:
        input = fd.read()
        print()
        print('ini data: ' + fname)
        print(input)


class TestGlobalSingle(unittest.TestCase):
    """Test parsing only global keys in single-value mode."""

    def test_globals1(self):
        '''Simple key value pairs.'''
        fname = 'tests/data/simple_global.ini'
        # ini_data(fname)
        ini = IniFile()
        ini.parse(fname)
        keys = ini.get_keys()
        self.assertTrue(keys[0] == 'home_page')
        self.assertTrue(keys[1] == 'email')
        self.assertTrue(keys[2] == 'you')
        self.assertTrue(keys[3] == 'them')
        value = ini.get_values('home_page')
        self.assertTrue(value == 'https://my.homepage.com')
        value = ini.get_values('email')
        self.assertTrue(value == 'me@ini.com')
        value = ini.get_values('you')
        self.assertTrue(value == 'you@your.com')
        value = ini.get_values('them')
        self.assertTrue(value == 'them@their.com')

    def test_globals2(self):
        '''True flags in the global section'''
        fname = 'tests/data/true_flag_globals.ini'
        ini = IniFile()
        ini.parse(fname)
        keys = ini.get_keys()
        # print()
        # print(keys)
        for key in keys:
            value = ini.get_values(key)
            # print()
            # print(key)
            # print(value)
            self.assertTrue(value)

    def test_globals3(self):
        '''True disjoint section and overriding multiple key names'''
        fname = 'tests/data/sections.ini'
        ini = IniFile()
        ini.parse(fname)
        sections = ini.get_sections()
        self.assertTrue(sections[0] == 'SECTION1')
        self.assertTrue(sections[1] == '_SECTION_')
        self.assertTrue(len(sections) == 2)
        keys = ini.get_section_keys(sections[0])
        self.assertTrue(len(keys) == 4)
        # first section values
        self.assertTrue(sections[0] == 'SECTION1')
        value = ini.get_section_values(sections[0], keys[0])
        self.assertTrue(value == 5)  # override of first value for this key
        value = ini.get_section_values(sections[0], keys[1])
        self.assertTrue(value == 2)
        value = ini.get_section_values(sections[0], keys[2])
        self.assertTrue(value == 3)
        value = ini.get_section_values(sections[0], keys[3])
        self.assertTrue(value == 4)
        # second section values
        keys = ini.get_section_keys(sections[1])
        self.assertTrue(sections[1] == '_SECTION_')
        value = ini.get_section_values(sections[1], keys[0])
        # print()
        # print(keys[0])
        # print(value)
        self.assertTrue(value == 50)  # override of first value for this key
        value = ini.get_section_values(sections[1], keys[1])
        self.assertTrue(value == 20)
        value = ini.get_section_values(sections[1], keys[2])
        self.assertTrue(value == 30)
        value = ini.get_section_values(sections[1], keys[3])
        self.assertTrue(value == 40)

    def test_globals4(self):
        '''Section and key names with all special characters.'''
        inistr = '''[SECTION_section_0123456789_!$%()*+-.<>?@^_{|}~]
KEY.key_10123456789_!$%()*+-.<>?@^_{|}~ = value
'''
        ini = IniFile()
        ini.parse(fstr=inistr)
        sections = ini.get_sections()
        self.assertTrue(
            sections[0] == 'SECTION_section_0123456789_!$%()*+-.<>?@^_{|}~')
        keys = ini.get_section_keys(sections[0])
        self.assertTrue(
            keys[0] == 'KEY.key_10123456789_!$%()*+-.<>?@^_{|}~')
        value = ini.get_section_values(sections[0], keys[0])
        self.assertTrue(value == 'value')

    def test_globals5(self):
        '''Quoted strings.'''
        fname = 'tests/data/quoted_strings.ini'
        ini = IniFile()
        ini.parse(fname)
        keys = ini.get_keys()
        # print()
        # print(keys)
        value = ini.get_values(keys[0])
        # print(value)
        self.assertTrue(value == 'my string, "baby"')
        value = ini.get_values(keys[1])
        # print(value)
        self.assertTrue(value == "double down, 'baby'")

    def test_globals6(self):
        '''Escaped characters.'''
        fname = 'tests/data/quoted_strings.ini'
        ini = IniFile()
        ini.parse(fname)
        keys = ini.get_keys()
        value = ini.get_values(keys[2])
        self.assertTrue(value[0] == 'a')
        self.assertTrue(value[1] == 'B')
        self.assertTrue(value[2] == '3')
        self.assertTrue(value[3] == '\\')
        self.assertTrue(value[4] == '"')
        self.assertTrue(value[5] == '#')
        self.assertTrue(value[6] == "'")
        self.assertTrue(value[7] == ',')
        self.assertTrue(value[8] == '/')
        self.assertTrue(value[9] == ':')
        self.assertTrue(value[10] == ';')
        self.assertTrue(value[11] == '=')
        self.assertTrue(value[12] == ' ')
        self.assertTrue(ord(value[13]) == 9)
        self.assertTrue(ord(value[14]) == 10)
        self.assertTrue(ord(value[15]) == 13)
        self.assertTrue(ord(value[16]) == 0xff)
        self.assertTrue(ord(value[17]) == 0x12ab)

    def test_globals7(self):
        '''Escaped characters in single-quoted string.'''
        fname = 'tests/data/quoted_strings.ini'
        ini = IniFile()
        ini.parse(fname)
        keys = ini.get_keys()
        value = ini.get_values(keys[3])
        self.assertTrue(value[0] == 'a')
        self.assertTrue(value[1] == 'B')
        self.assertTrue(value[2] == '3')
        self.assertTrue(value[3] == '\\')
        self.assertTrue(value[4] == '"')
        self.assertTrue(value[5] == '#')
        self.assertTrue(value[6] == "'")
        self.assertTrue(value[7] == ',')
        self.assertTrue(value[8] == '/')
        self.assertTrue(value[9] == ':')
        self.assertTrue(value[10] == ';')
        self.assertTrue(value[11] == '=')
        self.assertTrue(value[12] == ' ')
        self.assertTrue(ord(value[13]) == 9)
        self.assertTrue(ord(value[14]) == 10)
        self.assertTrue(ord(value[15]) == 13)
        self.assertTrue(ord(value[16]) == 0xff)
        self.assertTrue(ord(value[17]) == 0x12ab)

    def test_globals8(self):
        '''Escaped characters in double-quoted string.'''
        fname = 'tests/data/quoted_strings.ini'
        ini = IniFile()
        ini.parse(fname)
        keys = ini.get_keys()
        value = ini.get_values(keys[4])
        self.assertTrue(value[0] == 'a')
        self.assertTrue(value[1] == 'B')
        self.assertTrue(value[2] == '3')
        self.assertTrue(value[3] == '\\')
        self.assertTrue(value[4] == '"')
        self.assertTrue(value[5] == '#')
        self.assertTrue(value[6] == "'")
        self.assertTrue(value[7] == ',')
        self.assertTrue(value[8] == '/')
        self.assertTrue(value[9] == ':')
        self.assertTrue(value[10] == ';')
        self.assertTrue(value[11] == '=')
        self.assertTrue(value[12] == ' ')
        self.assertTrue(ord(value[13]) == 9)
        self.assertTrue(ord(value[14]) == 10)
        self.assertTrue(ord(value[15]) == 13)
        self.assertTrue(ord(value[16]) == 0xff)
        self.assertTrue(ord(value[17]) == 0x12ab)

    def test_globals9(self):
        '''Un-escaped characters in double-quoted string.'''
        fname = 'tests/data/quoted_strings.ini'
        ini = IniFile()
        ini.parse(fname)
        keys = ini.get_keys()
        value = ini.get_values(keys[5])
        self.assertTrue(value[0] == '#')
        self.assertTrue(value[1] == "'")
        self.assertTrue(value[2] == ',')
        self.assertTrue(value[3] == '/')
        self.assertTrue(value[4] == ':')
        self.assertTrue(value[5] == ';')
        self.assertTrue(value[6] == "=")
        self.assertTrue(value[7] == ' ')

    def test_globals10(self):
        '''Tortured line continues.'''
        fname = 'tests/data/quoted_strings.ini'
        ini = IniFile()
        ini.parse(fname)
        keys = ini.get_keys()
        value = ini.get_values(keys[6])
        self.assertTrue(value == 'double-continue')
        value = ini.get_values(keys[7])
        self.assertTrue(value == 'comment-continue')
        value = ini.get_values(keys[8])
        self.assertTrue(value == 'continue3')

    def test_globals11(self):
        '''Data from file handle.'''
        fname = 'tests/data/true_flag_globals.ini'
        with open(fname, 'r') as fd:
            ini = IniFile()
            ini.parse(fhandle=fd)
            keys = ini.get_keys()
            # print()
            # print(keys)
            for key in keys:
                value = ini.get_values(key)
                self.assertTrue(value)

    def test_globals12(self):
        '''Data from string.'''
        fname = 'tests/data/true_flag_globals.ini'
        with open(fname, 'r') as fd:
            input = fd.read()
            ini = IniFile()
            ini.parse(fstr=input)
            keys = ini.get_keys()
            # print()
            # print(keys)
            for key in keys:
                value = ini.get_values(key)
                self.assertTrue(value)


if __name__ == '__main__':
    unittest.main()
