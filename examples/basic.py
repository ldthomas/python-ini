''' @file examples/basic.py
@brief A very basic demonstration with a simple INI file.
'''

import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from python_ini.ini_file import IniFile

title = '''This is a very basic demonstration using a simple INI file.
It has only an anonymous, global section with no section names.
All keys are single valued. The keys are all listed along with their values.
'''
print()
print(title)

ini_file = '''
IP-address = 10.87.1.209    ; string
name = "Sam Johnson"        ; double-quoted string
$(funny-key)%: 'Joe Blow'   ; single-quoted string, colon key/value separator
number = 100                ; integer number
false-flag = false          ; boolean
true-flag                   ; boolean true flag (no value default)
'''
# parse the file in single-value mode
ini = IniFile()
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
    print(values)
print()
