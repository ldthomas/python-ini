''' @file examples/multi_values.py
@brief A demonstration of keys with multiple values.
'''

import sys
import os
from pprint import pprint
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from python_ini.ini_file import IniFile

title = '''This example demonstrates multi-value mode.
Key values are lists of multiple values.
The keys are all listed along with their values.
'''
print()
print(title)

ini_file = '''
IP-addresses = 10.87.1.209, 127.0.0.1
name = "Sam Johnson"        ; single value is still a list
$(funny-key)%: 'Joe Blow'
$(funny-key)%: 'Jimmy Bob'  ; multiple occurrances of a key are concatenated to a single list
numbers = 100, 200, 300      ; numbers, not strings
booleans = true, yes, on, false, no, off, null, void, none
'''
# parse the file in multi-value mode
ini = IniFile('m')
ini.parse(fstr=ini_file)
if(ini.errors):
    print(ini.display_errors())

# get a list of key names
keys = ini.get_keys()
print('all keys and values')
for key in keys:
    # get the value for each key
    values = ini.get_values(key)
    print(key, end=': ')
    pprint(values)
print()
