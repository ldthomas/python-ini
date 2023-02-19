''' @file examples/writer.py
@brief A demonstration of the INI writer.
'''

import sys
import os
sys.path.append(os.getcwd())  # required to find python_ini
from python_ini.ini_file import IniFile
from python_ini.ini_writer import IniWriter
w = IniWriter()

# set all configurable values
w.delimiters('#', ':', ',')
w.booleans('TRUE', 'OFF', 'void')
w.comment_tab(30)

# global keys
w.comment()
w.comment('global keys')
w.key('Unicode', 'a\U0010ffffb', 'max Unicode character')
w.key('flags', [True, False, None], 'all "booleans"')

# section keys
w.comment()
w.comment('first section')
w.section('__SECTION__', 'this is a section')
w.key('section_key', [1, 2, 3])
w.key(
    'long-key',
    ['abc\xffdef\ue000ghi\U0010ffffjkl'],
    'hex and Unicode string characters')

# print the formatted INI file
print(w.to_string())

# write the formatted INI file, parse it and remove it
fname = 'output.ini'
w.write(fname)
ini = IniFile('m')
ini.parse(fname)
if(ini.errors):
    print('parsing errors in file ' + fname)
    print(ini.display_errors())
else:
    print('INI file ' + fname + ' parsed without errors')
os.remove(fname)
print('INI file ' + fname + ' removed')
