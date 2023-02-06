''' @file examples/all_options.py
@brief A demonstration of almost all of the features of the IniFile class.
'''

import sys
import os
from pprint import pprint
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from python_ini.ini_file import IniFile
fname = 'examples/data.ini'

title = '''This example demonstrates almost all of the features of python-ini.
The INI file is displayed. It is commented to explain all of the optional
features available. The INI parser is then used to display all sections,
keys and values.
'''
print()
print(title)
print()
print('----- INI FILE BEGIN -----')
with open(fname, 'r') as fd:
    ini = fd.read()
    print(ini)
print('----- INI FILE END -----')

# parse the file in single-value mode
ini = IniFile()
ini.parse(fname)
if(ini.errors):
    print(ini.display_errors())
# get a list of key names
keys = ini.get_keys()
print()
print('SINGLE-VALUE MODE ANONYMOUS KEYS AND VALUES')
for key in keys:
    # get the value for eack key
    values = ini.get_values(key)
    print(key, end=': ')
    print(values)
# get a list of section names
sections = ini.get_sections()
print()
print('SINGLE-VALUE MODE SECTION NAMES, KEYS AND VALUES')
for section in sections:
    # get a list of key names for each section
    keys = ini.get_section_keys(section)
    for key in keys:
        # get the value for each section key
        values = ini.get_section_values(section, key)
        print('[' + section + ']:' + key, end=' ')
        print(values)
# parse the file in multi-value mode
ini = IniFile('m')
ini.parse(fname)
if(ini.errors):
    print(ini.display_errors())
# get a list of key names
keys = ini.get_keys()
print()
print('MULTI-VALUE MODE ANONYMOUS KEYS AND VALUES')
for key in keys:
    # get the list of values for each key
    values = ini.get_values(key)
    print(key, end=': ')
    pprint(values)
# get a list of section names
sections = ini.get_sections()
print()
print('MULTI-VALUE MODE SECTION NAMES, KEYS AND VALUES')
for section in sections:
    # get a list of keys for each section
    keys = ini.get_section_keys(section)
    for key in keys:
        # get a list of values for each section key
        values = ini.get_section_values(section, key)
        print('[' + section + ']:' + key, end=' ')
        pprint(values)
