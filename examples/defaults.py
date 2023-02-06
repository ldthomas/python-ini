''' @file examples/defaults.py
@brief A demonstration of specifying default values for missing section or key names.
'''

import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from python_ini.ini_file import IniFile

title = '''This example demonstrates the use of default values for specific keys.
Some requests are for section names and keys that do not exist in the INI file.
In these cases default values are specified. Note that default values are passed
through exactly as specified and may not have the same characteristics of valid
key values.
'''
print()
print(title)

ini_file = '''
[SECTION.1]
number = 100
name = "Sam Johnson"
false-flag = false
[SECTION.1.1]
number = 200
flag
'''
# parse the file in single-value mode
ini = IniFile()
ini.parse(fstr=ini_file)
if(ini.errors):
    print(ini.display_errors())

# request an anonymous key, but none exist
key = 'non-existant'
values = ini.get_values(key, default=100)
print('request an anonymous key that does not exist')
print(key, end=': ')
print(values)

# default is not an ordinarily valid key value
print('\nrequest with default that is not an ordinarily valid value')
key = 'non-existant'
values = ini.get_values(key, default={'invalid': 100})
print(key, end=': ')
print(values)

# a couple of valid values
section = 'SECTION.1'
key = 'number'
values = ini.get_section_values(section, key, default=300)
print('\nrequest a couple of valid section/key values')
print(section, end=', ')
print(key, end=': ')
print(values)
section = 'SECTION.1.1'
key = 'number'
values = ini.get_section_values(section, key, default=300)
print(section, end=', ')
print(key, end=': ')
print(values)

# section doen't exist
section = 'SECTION.2'
key = 'number'
values = ini.get_section_values(section, key, default=300)
print('\nsection doesn\'t exist')
print(section, end=', ')
print(key, end=': ')
print(values)

# key doen't exist
section = 'SECTION.1'
key = 'flag'
values = ini.get_section_values(section, key, default=False)
print('\nkey doesn\'t exist')
print(section, end=', ')
print(key, end=': ')
print(values)
