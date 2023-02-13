## A Quick Start INI Writer Example from the GitHub Installation

### The Project Structure

Throughout this example we will assume the project structure:

```bash
|my_project_folder
|---|python-ini-main.zip
    |my_project
    |---__init__.py
    |---write.py
```

All commands will be executed from the `my_project_folder` directory.
The content of the files will be presented and explained as we go.

### Installation

Make sure the PyPI version of `python-ini` is not installed.
Otherwise it will override the local GitHub version. However, `apg-py` must be installed.

```bash
pip uninstall python-ini
pip install apg-py
```

Install the GitHub version of `python-ini`.

```bash
unzip python-ini-main.zip
cp -r python-ini-main/python_ini .
```

### The Creat, Print and Write an INI file

The code , `write.py` could look somthing like this.

```python
import sys
import os
sys.path.append(os.getcwd()) # required to find python_ini
from python_ini.ini_writer import IniWriter
from python_ini.ini_file import IniFile

# set all configurable values
w = IniWriter()
w.delimiters('#', ':', ',')
w.booleans('TRUE', 'OFF', 'void')
w.comment_tab(30)

# the global keys
w.comment()
w.comment('global keys')
w.key('key0', 'a\U0010ffffb', 'max Unicode character')
w.key('key1', 1, 'key1 comment')
w.key('key2', True)
w.key('key4', False)
w.key('key5', None)
w.key('key3', 'true')

# section keys
w.comment()
w.comment('first section')
w.section('__SECTION__', 'this is a section')
w.key('section_key1', [1, 2, 3])
w.key('section_key2', ['true', True, 1e12])
w.key(
    'section_key3',
    ['abc\xffdef\ue000ghi\U0010ffffjkl'],
    'hex and Unicode string characters')

# print the formatted INI file
s = w.to_string()
print(s)

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
```

Execute the command:

```bash
python3 my_project/write.py
```

You should see the results:

```

# global keys
key0: 'a\U0010ffffb'          # max Unicode character
key1: 1                       # key1 comment
key2: TRUE
key4: OFF
key5: void
key3: 'true'

# first section
[__SECTION__]                 # this is a section
section_key1: 1, 2, 3
section_key2: 'true', TRUE, 1000000000000.0
section_key3: 'abc\xffdef\ue000ghi\U0010ffffjkl'
                              # hex and Unicode string characters

INI file output.ini parsed without errors
INI file output.ini removed
```
