''' @file python_ini/help.py
@brief This is the INI help function.
<pre>
options:
  -h, --help            show this help message and exit
  -v, --version         display the version and copyright information

</pre>
'''
# import os
# import sys
import argparse
# sys.path.append(os.getcwd())
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'


desc = '''
This is a Python INI file parser.
'''
ep = '''NOTES: ???
'''

how_to = '''usage: implemented as a Python class with member functions to parse and retrieve key values
See the full documentation at https://sabnf.com/docs/ini/index.html for complete details.
A simple Python program illustrating the basics follows.

from python_ini.ini_file import IniFile
ini = IniFile()                                 # default is single-value mode
ini.parse(INI_FILE_NAME)
if(ini.errors):
    print('INI FILE ERRORS')
    print(ini.display_errors())                 # display any errors found in the INI file
keys = ini.get_keys()                           # get a list of all keys in the global section
for key in keys:
    values = ini.get_values(key)                # get the value for each key
    print(key, end=': ')
    print(values)
sections = ini.get_sections()                   # get a list of all section names
for section in sections:
    keys = ini.get_section_keys(section)        # get a list of all keys in each section
        for key in keys:
            values = ini.get_section_values(section, key)   # get the value for each section key
            print('[' + section + ']:' + key, end=' ')
            print(values)
'''


def main():
    parser = argparse.ArgumentParser(
        prog='python-ini',
        description=desc
    )
    parser.add_argument('-v', '--version',
                        help='display the version and copyright information and exit',
                        dest='version',
                        action='store_true')
    parser.add_argument('-u', '--usage',
                        help='display INI file parser usage and exit',
                        dest='usage',
                        action='store_true')
    args = parser.parse_args()

    if(args.version):
        # handle the version request
        text = 'python-ini version 1.0'
        text += '\nA Python INI file parser'
        text += '\nCopyright (c) 2023 Lowell D. Thomas'
        print(text)
        exit()

    if(args.usage):
        # input SABNF file name required
        print(how_to)
        exit()

    print('options [--help | --version | --usage]')
